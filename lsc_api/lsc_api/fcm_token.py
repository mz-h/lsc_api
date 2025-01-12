import firebase_admin
from firebase_admin import credentials, messaging
import frappe
import json
import re
from frappe.realtime import emit_via_redis

# from lsc_api.lsc_api.comment_notification import comment_notification


def remove_html_tags(text):
    """
    Removes HTML tags from the given text.

    Args:
        text (str): The text from which HTML tags need to be removed.

    Returns:
        str: The text without HTML tags.
    """
    clean = re.compile("<.*?>")  # Regular expression to match HTML tags
    return re.sub(clean, "", text)


def send_comment_notification(doc, method):
    # comment_notification(doc, method)
    # if not frappe.db.exists(doc.doctype, doc.name):
    #     return

    try:
        doctype_list = ["Case", "Cases Study", "Legal Service", "Consultation"]

        subject = remove_html_tags(
            str(doc.subject) if doc.subject else "No Content, Have a nice day!"
        )
        message_content = (
            remove_html_tags(str(doc.content))
            if doc.content
            else "No Content, Have a nice day!"
        )
        doctype = doc.reference_doctype
        document_name = doc.reference_name
        if frappe.db.exists(doctype, document_name):
            doc_doc = frappe.get_doc(doctype, document_name)

            if doc.comment_type in ["Comment", "Attachment"]:
                emit_via_redis(
                    str(doc_doc.client_transaction) if doctype in doctype_list else "hello",
                    {
                        "creation": doc.creation,
                        "comment_type": doc.comment_type,
                        "content": message_content,
                        "owner": doc.owner,
                    },
                    None,
                )

    except Exception as e:
        frappe.log_error(
            f"Error in send_comment_notification: {str(e)}", "Comment Notification"
        )


def send_firebase_notification(doc, method):
    subject = remove_html_tags(
        str(doc.subject) if doc.subject else "No Content, Have a nice day!"
    )
    message_content = (
        remove_html_tags(str(doc.email_content))
        if doc.email_content
        else "No Content, Have a nice day!"
    )
    doctype = doc.document_type
    document_name = doc.document_name

    emit_via_redis(
        doc.for_user,
        {
            "subject": subject,
            "message_content": message_content,
            "doctype": doctype,
            "document_name": document_name,
            "user": doc.for_user,
        },
        None,
    )

    device_tokens = []
    query = frappe.get_list(
        "Notifications Token", filters={"user": doc.for_user}, fields=["token"]
    )
    for row in query:
        device_tokens.append(row["token"])

    if not device_tokens:
        frappe.log_error(
            message=f"No device tokens found for user: {doc.for_user}",
            title=f"No device tokens found for user: {doc.for_user}",
        )
        return

    # Get and validate Firebase settings
    try:
        firebase_settings = frappe.get_doc("Firebase Settings")
        if not firebase_settings or not firebase_settings.private_key:
            frappe.log_error(
                message="Firebase settings not configured or private key missing",
                title="Firebase Configuration Error"
            )
            return

        # Get the file name from private key path
        private_key_path = firebase_settings.private_key
        if not private_key_path or '/' not in private_key_path:
            frappe.log_error(
                message=f"Invalid private key path: {private_key_path}",
                title="Firebase Configuration Error"
            )
            return

        json_file_path = frappe.get_site_path(
            "private", "files", private_key_path.split("/")[-1]
        )

        # Check if file exists
        if not os.path.exists(json_file_path):
            frappe.log_error(
                message=f"Firebase credentials file not found at: {json_file_path}",
                title="Firebase Configuration Error"
            )
            return

    except Exception as e:
        frappe.log_error(
            message=f"Error accessing Firebase settings: {str(e)}",
            title="Firebase Configuration Error"
        )
        return

    # Load the JSON credentials from the file
    try:
        with open(json_file_path) as f:
            firebase_creds = json.load(f)
    except Exception as e:
        frappe.log_error(
            title="Failed to load Firebase credentials",
            message=f"Failed to load Firebase credentials: {str(e)}"
        )
        return

    # Initialize Firebase app using the credentials
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
    except Exception as e:
        frappe.log_error(
            title="Failed to initialize Firebase",
            message=f"Failed to initialize Firebase: {str(e)}"
        )
        return

    # Loop through the device tokens and send notifications
    for token in device_tokens:
        message = messaging.Message(
            notification=messaging.Notification(title=subject, body=message_content),
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(sound="default")
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(aps=messaging.Aps(sound="default"))
            ),
            token=token,
            data={
                "doctype": doctype,
                "document_name": document_name,
            },
        )

        try:
            response = messaging.send(message)
        except Exception as e:
            frappe.log_error(
                message=f"Failed to send notification to token {token}: {str(e)}",
                title="Failed to send notification to token"
            )