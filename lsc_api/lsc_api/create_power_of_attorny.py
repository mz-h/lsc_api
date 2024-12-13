import frappe
from frappe.utils.file_manager import save_file
from frappe.utils import now_datetime


@frappe.whitelist(methods=["POST"])
def create_power_of_attorny(**kwargs):
    user = frappe.session.user

    if frappe.db.exists("Customer", {"custom_user": user}):
        customer = frappe.get_doc("Customer", {"custom_user": user})
    else:
        return {"status": "fail", "message": "Customer not found"}

    lawyer = kwargs.get("lawyer")
    najiz_number = kwargs.get("attonery_number__najiz")
    expiry_date = kwargs.get("expiry_date")
    doc_content = kwargs.get("attorney_content")

    if not frappe.db.exists("Employee", {"name": lawyer}):
        return {"status": "fail", "message": "Lawyer not found"}

    poa = frappe.new_doc("Power of Attornies")
    poa.client = customer.name
    poa.lawyer = lawyer
    poa.attonery_number__najiz = najiz_number
    poa.expiry_date = expiry_date
    poa.attorney_content = doc_content
    poa.save(ignore_permissions=True)

    client_transactions = frappe.get_all(
        "Client Transaction",
        {"status": ["in", ["New", "On Hold", "In Progress"]], "client": customer.name},
        "*",
    )

    for transaction in client_transactions:
        transaction.poa_exp_date = poa.expiry_date

    uploaded_file = frappe.request.files.get("file")
    if uploaded_file:
        original_filename = uploaded_file.filename
        timestamp = now_datetime().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}_{original_filename}"

        content = uploaded_file.read()
        saved_file = save_file(
            unique_filename,
            content,
            poa.doctype,
            poa.name,
            is_private=1,
        )

        poa.append("table_dflf", {"attachments": saved_file.file_url})

        poa.save(ignore_permissions=True)

    return {
        "status": "success",
        "client": customer.name,
        "lawyer": lawyer,
        "attonery_number__najiz": najiz_number,
        "attorney_content": doc_content,
        "expiry_date": expiry_date,
    }
