import frappe
from frappe.utils.file_manager import save_file
from frappe.utils import now_datetime


@frappe.whitelist(methods=["GET"])
def get_paid_invoices():
    user = frappe.session.user

    if frappe.db.exists("Customer", {"custom_user": user}):
        customer = frappe.get_doc("Customer", {"custom_user": user})
    else:
        return {"status": "fail", "message": "Customer not found"}

    responses = frappe.get_all(
        "Sales Invoice",
        {"customer": customer.name, "status": "Paid"},
        ["total", "currency", "name", "creation"],
    )

    for response in responses:
        response["print_format"] = (
            f"https://lsc.psc-s.com/printview?doctype=Sales%20Invoice&name={response.name}&trigger_print=1&format=KSA%20VAT%20Invoice%20QR&no_letterhead=0&letterhead=LSC%20Head&settings=%7B%7D&_lang=en"
        )
        item = frappe.get_all(
            "Sales Invoice Item", {"parent": response.name}, "item_name"
        )
        response["item"] = item
        del response["name"]

    if responses:
        return {"status": "success", "data": responses}
    else:
        return {"status": "success", "data": [], "message": "There are no invoices"}
