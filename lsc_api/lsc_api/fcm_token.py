import firebase_admin
from firebase_admin import credentials, messaging
import frappe
import json
import re

def remove_html_tags(text):
    """
    Removes HTML tags from the given text.
    
    Args:
        text (str): The text from which HTML tags need to be removed.
        
    Returns:
        str: The text without HTML tags.
    """
    clean = re.compile('<.*?>')  # Regular expression to match HTML tags
    return re.sub(clean, '', text)


def send_firebase_notification(doc, method):
    subject = remove_html_tags(doc.subject)
    message_content = remove_html_tags(doc.email_content) if doc.email_content else "No Content, Have a nice day!"
    doctype = doc.document_type
    document_name = doc.document_name

    #-----Get Device Tokens-----#
    device_tokens = []
    query = frappe.get_list("Notifications Token",
        filters={"user": doc.for_user},
        fields=["token"]
    )
    for row in query:
        device_tokens.append(row["token"])

    if not device_tokens:
        frappe.log_error(message=f"No device tokens found for user: {doc.for_user}",
                              title=f"No device tokens found for user: {doc.for_user}")
        return
    
    # Get the Firebase settings
    firebase_settings = frappe.get_doc("Firebase Settings")
    json_file_path = frappe.get_site_path('private', 'files', firebase_settings.private_key.split("/")[-1])

    # Load the JSON credentials from the file
    try:
        with open(json_file_path) as f:
            firebase_creds = json.load(f)
    except Exception as e:

        frappe.log_error(message=f"Failed to load Firebase credentials",
                    title=f"Failed to load Firebase credentials: {str(e)}")
        return
    
    # Initialize Firebase app using the credentials
    if not firebase_admin._apps:  # This prevents re-initialization errors
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)

    # Loop through the device tokens and send notifications
    for token in device_tokens:
        message = messaging.Message(
            notification=messaging.Notification(
                title=subject,
                body=message_content
            ),
            token=token,  # Sending to the specific device token
            data={  # Add custom data
                "doctype": doctype,
                "document_name": document_name
            }
        )
        
        # Send the notification
        try:
            response = messaging.send(message)
            frappe.log_error(message=f"Successfully sent notification to token {token}: {str(response)}",
                              title="Successfully sent notification to token")
        except Exception as e:
            frappe.log_error(message=f"Failed to send notification to token {token}: {str(e)}",
                              title="Failed to send notification to token")
