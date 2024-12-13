import frappe
__version__ = "0.0.1"


def fetch_notofications():
    user = frappe.session.user
    notifications = frappe.get_all(
        "Notification Log",
        filters={
            "for_user": user,
        },
        fields=[
            "name",
            "subject",
            "type",
            "document_type",
            "document_name",
            "creation",
        ],
        order_by="creation desc",
    )
    frappe.publish_realtime(
        'fetch_notofications',
        {'notifications': notifications},
    )
