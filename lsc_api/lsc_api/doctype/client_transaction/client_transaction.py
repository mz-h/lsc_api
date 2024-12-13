# Copyright (c) 2024, M and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import today, date_diff


class ClientTransaction(Document):
    def validate(self):
        diff_in_days = 0

        on_hold_settings = frappe.get_doc("Notify On Hold")
        if self.status == "On Hold" and not self.on_hold_date:
            self.on_hold_date = today()

        if self.status == "On Hold" and self.on_hold_date:
            diff_in_days = date_diff(today(), self.on_hold_date)

        if self.status != "On Hold":
            self.on_hold_date = None
            self.on_hold_check = 0


        if frappe.db.exists("Case", {"client_transaction": self.name}):
            frappe.db.set_value("Case", {"client_transaction": self.name}, "client_transaction_status", self.status)
            

        if frappe.db.exists(
            "Cases Study", {"client_transaction": self.name}
        ):
            frappe.db.set_value("Cases Study", {"client_transaction": self.name}, "client_transaction_status", self.status)


        if frappe.db.exists(
            "Legal Service", {"client_transaction": self.name}
        ):
            frappe.db.set_value("Legal Service", {"client_transaction": self.name}, "client_transaction_status", self.status)
            

        if frappe.db.exists(
            "Consultation", {"client_transaction": self.name}
        ):
            frappe.db.set_value("Consultation", {"client_transaction": self.name}, "client_transaction_status", self.status)
            


@frappe.whitelist()
def create_task(source_name, target_doc=None):
    return get_mapped_doc(
        "Client Transaction",
        source_name,
        {
            "Client Transaction": {
                "doctype": "Task",
                "field_map": {
                    "name": "custom_client_transaction",
                    "employee": "custom_employee",
                },
            }
        },
        target_doc,
    )
