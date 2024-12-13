# Copyright (c) 2024, M and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class Consultation(Document):
    def after_insert(self):
        check_and_update_subscription(self)
        self.create_appointment()

    def create_appointment(self):
        appointment_settings = frappe.get_doc("Notify On Hold")
        item = frappe.db.get_value("Client Transaction", self.client_transaction, "item")
        if item != "استشارة كتابية":
            available_employee = self.get_available_employee(self.date, self.start_time)
            if available_employee:
                cur_employee = frappe.get_doc({
                    "doctype": "Employee Appointment",
                    "customer": self.client,
                    "employee": available_employee,
                    "appointment_type": appointment_settings.default_employee_appointment_type,
                    "duration": frappe.db.get_value(
                        "Employee Appointment Type",
                        appointment_settings.default_employee_appointment_type,
                        "default_duration",
                    ),
                    "appointment_for": "Employee",
                    "appointment_date": self.date,
                    "appointment_time": self.start_time,
                    "consultation": self.name,
                    "mode_of_payment": "",
                    "paid_amount": "",
                    "invoiced": 0,
                })
                cur_employee.insert(ignore_permissions=True)

                # Assign task to the employee if user_id is found
                emp_user = frappe.db.get_value("Employee", available_employee, "user_id")
                if emp_user:
                    cs = frappe.get_doc({
                        "doctype": "ToDo",
                        "allocated_to": emp_user,
                        "reference_type": "Consultation",
                        "reference_name": self.name,
                        "description": "Consultation Employee Assignment.",
                        "status": "Open",
                        "assigned_by": frappe.session.user,
                    })
                    cs.insert(ignore_permissions=True)
                else:
                    frappe.log_error(f"No user linked to employee {available_employee}", "Consultation Error")
            else:
                frappe.throw("No available employees found for this appointment time.")

    def get_available_employee(self, date, start_time):
        # Fetch all employees with schedules
        employees = frappe.get_all("Employee", fields=["name", "employee_name"])
        
        for employee in employees:
            # Check if employee has overlapping appointments
            overlap = frappe.db.sql("""
                SELECT name FROM `tabEmployee Appointment`
                WHERE employee = %s
                AND appointment_date = %s
                AND appointment_time <= %s
                AND ADDTIME(appointment_time, SEC_TO_TIME(duration*60)) > %s
                AND docstatus != 2
            """, (employee['name'], date, start_time, start_time))
            if not overlap:
                return employee['name']
        
        # If no available employees found
        return None


    @frappe.whitelist()
    def set_employee(self, employee):
        # Get the Employee Appointment linked to the consultation
        appointment_name = frappe.db.get_value("Employee Appointment", {"consultation": self.name}, "name")

        if not appointment_name:
            frappe.throw(_("No appointment found linked to this consultation."), title=_("Error"))

        try:
            # Fetch the appointment document by name
            appointment = frappe.get_doc("Employee Appointment", appointment_name)

            cancel_existing_todo_for_consultation(self.name)
            # Cancel the appointment by updating its status and calling the cancellation logic
            frappe.db.set_value("Employee Appointment", appointment.name, "status", "Cancelled")
            cancel_appointment(appointment.name)

            # Ensure the new employee exists
            new_employee_doc = frappe.get_doc("Employee", employee)

            # Create a new appointment with the same details but assign the new employee
            new_appointment = frappe.copy_doc(appointment)
            new_appointment.employee = employee
            new_appointment.insert(ignore_permissions=True)

            # Cancel the existing ToDo assigned to the current employee

            # Assign a new ToDo to the newly assigned employee user
            emp_user = frappe.db.get_value("Employee", employee, "user_id")
            if emp_user:
                new_todo = frappe.get_doc({
                    "doctype": "ToDo",
                    "allocated_to": emp_user,
                    "reference_type": "Consultation",
                    "reference_name": self.name,
                    "description": _("Consultation reassigned to {0}").format(new_employee_doc.employee_name),
                    "status": "Open",
                    "assigned_by": frappe.session.user,
                })
                new_todo.insert(ignore_permissions=True)

            # Log the change
            frappe.msgprint(
                _("Consultation {0} has been reassigned to {1}").format(
                    new_appointment.name, new_employee_doc.employee_name
                ),
                title=_("Employee Reassigned"),
            )

        except frappe.DoesNotExistError:
            frappe.throw(_("The appointment or employee you are trying to modify does not exist."), title=_("Error"))
        except Exception as e:
            frappe.log_error(f"Error reassigning employee in appointment: {str(e)}", "Set Employee Error")
            frappe.throw(_("There was an issue updating the employee for the appointment. Please try again."), title=_("Error"))

def cancel_existing_todo_for_consultation(consultation):
    try:
        # Fetch and cancel the ToDo assigned to the original employee for this appointment
        todos = frappe.get_all("ToDo", filters={"reference_name": consultation, "reference_type": "Consultation", "status": "Open"}, fields=["name"])
        for todo in todos:
            frappe.db.set_value("ToDo", todo.name, "status", "Cancelled")
    except Exception as e:
        frappe.log_error(f"Error cancelling ToDo for Consultation {consultation}: {str(e)}", "Cancel ToDo Error")


def check_and_update_subscription(doc):
    client_transaction = frappe.get_doc("Client Transaction", doc.client_transaction)
    client = client_transaction.client

    # Fetch active subscription for the client
    subscription = frappe.get_all(
        "Subscription", filters={"party": client, "status": "Active"}, fields=["name"]
    )

    if not subscription:
        frappe.throw(f"No active subscription found for client {client}")

    subscription_name = subscription[0].name
    subscription_doc = frappe.get_doc("Subscription", subscription_name)

    # Fetch subscription plan details
    plan_name = subscription_doc.plans[0].plan
    subscription_plan = frappe.get_doc("Subscription Plan", plan_name)

    # Check if item is in allowed services
    allowed_services = [
        service.service_name for service in subscription_plan.custom_allowed_services
    ]
    if client_transaction.item not in allowed_services:
        frappe.throw(
            f"Service {client_transaction.item} is not allowed in the subscription plan"
        )

    # Fetch hours required for the service from Plans Setting
    plans_setting = frappe.get_doc("Plans Settings", "Plans Settings")
    service_settings = {
        setting.service_name: setting.hrs for setting in plans_setting.service_settings
    }

    if client_transaction.item not in service_settings:
        frappe.throw(f"Service {client_transaction.item} not found in Plans Setting")

    required_hours = float(service_settings[client_transaction.item])

    # Check if enough hours are available in the subscription custom quota
    consultation_quota = None
    for quota in subscription_doc.custom_quota:
        if quota.service_name == "ساعات الاستشارة":
            consultation_quota = quota
            break

    if not consultation_quota:
        frappe.throw(f"No consultation hours quota found in the subscription")

    available_hours = float(consultation_quota.hrs)

    if available_hours < required_hours:
        frappe.throw(
            f"Not enough hours available. Required: {required_hours}, Available: {available_hours}"
        )

    # Deduct the hours from the quota and format as integer
    updated_hours = int(available_hours - required_hours)
    consultation_quota.hrs = str(updated_hours)

    # Update consumed hours
    consumed_hours = float(consultation_quota.consumed_hrs or 0)
    consultation_quota.consumed_hrs = str(int(consumed_hours + required_hours))

    subscription_doc.save()

def cancel_appointment(appointment_id):
    appointment = frappe.get_doc("Employee Appointment", appointment_id)
    msg = _("Appointment Cancelled.")
    if appointment.event:
        event_doc = frappe.get_doc("Event", appointment.event)
        event_doc.status = "Cancelled"
        event_doc.save()

    frappe.msgprint(msg)
