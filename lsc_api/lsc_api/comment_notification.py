import frappe
from frappe import permissions


def comment_notification(doc, method):
    # if not frappe.db.exists(doc.doctype, doc.name):
    #     return
    
    try:
        if doc.reference_doctype in [
            "Case",
            "Cases Study",
            "Consultation",
            "Legal Service",
        ]:
            if frappe.db.exists(doc.reference_doctype, doc.reference_name):
                
                ref_doc = frappe.get_doc(doc.reference_doctype, doc.reference_name)
                owner = ref_doc.owner

                # Check if client_transaction exists and is not None
                client_transaction = getattr(ref_doc, 'client_transaction', None)
                if not client_transaction:
                    frappe.log_error(
                        f"No client transaction found for {doc.reference_doctype} {doc.reference_name}",
                        "Comment Notification"
                    )
                    return

                assigned_users = frappe.get_all(
                    "ToDo",
                    filters={
                        "reference_type": doc.reference_doctype,
                        "reference_name": doc.reference_name,
                        "status": "Open",
                    },
                    fields=["allocated_to"],
                )
                assigned_user_list = [user["allocated_to"] for user in assigned_users]

                if (
                    owner
                    and owner != doc.owner
                    and doc.comment_type in ["Comment", "Attachment"]
                ):
                    lang = frappe.db.get_value("User", {"name": owner}, "language")
                    
                    notification_data = {
                        "doctype": "Notification Log",
                        "type": "Alert",
                        "document_type": "Client Transaction",
                        "document_name": client_transaction,
                        "for_user": owner,
                    }

                    if lang == "ar":
                        notification_data.update({
                            "subject": f"تعليق جديد على {ref_doc.name}",  # Using name instead of str(ref_doc)
                            "email_content": f"تعليق جديد على: {doc.content}",
                        })
                    else:
                        notification_data.update({
                            "subject": f"New Comment on {ref_doc.name}",  # Using name instead of str(ref_doc)
                            "email_content": f"A new comment has been added: {doc.content}",
                        })

                    notification = frappe.get_doc(notification_data)
                    notification.insert(ignore_permissions=True)
                    frappe.db.commit()

    except Exception as e:
        frappe.log_error(
            f"Error in comment_notification: {str(e)}\nTraceback: {frappe.get_traceback()}",
            "Comment Notification"
        )


# def edit_share_checks(doc, method):
#     doc.write = 1
#     doc.share = 1
#     doc.save(ignore_permissions=True)
