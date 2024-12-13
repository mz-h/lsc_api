# Copyright (c) 2024, M and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CasesStudy(Document):
    def after_insert(self):
        client_transaction = frappe.get_doc(
            "Client Transaction", self.client_transaction
        )
        client = client_transaction.client

        # Fetch active subscription for the client
        subscription = frappe.get_all(
            "Subscription",
            filters={"party": client, "status": "Active"},
            fields=["name"],
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
            service.service_name
            for service in subscription_plan.custom_allowed_services
        ]

        if client_transaction.item not in allowed_services:
            frappe.throw(
                f"Service {client_transaction.item} is not allowed in the subscription plan"
            )

        # Fetch hours required for the service from Plans Setting
        plans_setting = frappe.get_doc("Plans Settings", "Plans Settings")
        service_settings = {
            setting.service_name: setting.hrs
            for setting in plans_setting.service_settings
        }

        if client_transaction.item not in service_settings:
            frappe.throw(
                f"Service {client_transaction.item} not found in Plans Setting"
            )

        required_hours = float(service_settings[client_transaction.item])

        # Check if enough hours are available in the subscription custom quota
        cases_quota = None
        for quota in subscription_doc.custom_quota:
            if quota.service_name == "ساعات القضايا":
                cases_quota = quota
                break

        if not cases_quota:
            frappe.throw(f"No cases hours quota found in the subscription")

        available_hours = float(cases_quota.hrs)

        if available_hours < required_hours:
            frappe.throw(
                f"Not enough hours available. Required: {required_hours}, Available: {available_hours}"
            )

        # Deduct the hours from the quota and format as integer
        updated_hours = int(available_hours - required_hours)
        cases_quota.hrs = str(updated_hours)

        # Update consumed hours
        consumed_hours = float(cases_quota.consumed_hrs or 0)
        cases_quota.consumed_hrs = str(int(consumed_hours + required_hours))

        subscription_doc.save()
