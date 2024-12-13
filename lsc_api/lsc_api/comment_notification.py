import frappe


def comment_notification(doc, method):
    if doc.reference_doctype in [
        "Case",
        "Cases Study",
        "Consultation",
        "Legal Service",
    ]:
        ref_doc = frappe.get_doc(doc.reference_doctype, doc.reference_name)

        owner = ref_doc.owner

        if owner:
            notification = frappe.get_doc(
                {
                    "doctype": "Notification Log",
                    "subject": f"New Comment on {ref_doc}",
                    "type": "Alert",
                    "email_content": f"A new comment has been added: {doc.content}",
                    "document_type": ref_doc,
                    "document_name": ref_doc.name,
                    "for_user": owner,
                }
            )
            notification.insert(ignore_permissions=True)
            frappe.db.commit()
