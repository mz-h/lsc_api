import frappe
import requests
import random
import re
import json
from TaqnyatSms import client

otp = None
phone_number = None


@frappe.whitelist(allow_guest=True)
def sms_api(**kwargs):
    global otp
    global phone_number

    phone_number = kwargs.get("phone_number")

    if phone_number is None:
        return {
            "status": "fail",
            "message": "Phone number is required.",
        }

    if not is_valid_phone_number(phone_number):
        return {
            "status": "fail",
            "message": "Invalid phone number format. Please provide a valid number.",
        }

    bearer_token = "45e5c7c48191852bb9933f8931e08536"
    otp = generate_otp()
    sender = "Taqnyat.sa"
    body = f"Your OTP is {otp}."
    recipients = [phone_number]

    taqnyt = client(bearer_token)
    message = taqnyt.sendMsg(body, recipients, sender, scheduled=None)

    if isinstance(message, str):
        try:
            response = json.loads(message)
        except json.JSONDecodeError as e:
            return {
                "status": "fail",
                "message": f"Error decoding JSON response: {str(e)}",
            }
    else:
        response = message

    if response.get("statusCode") == 201:
        return {"status": "success", "message": "OTP sent successfully!", "otp": otp}
    else:
        return {
            "status": "fail",
            "message": f"Failed to send OTP. Error: {response}",
        }


def generate_otp():
    return str(random.randint(100000, 999999))


def is_valid_phone_number(phone_number):
    pattern = r"^9665[0-9]{8}$"
    return re.match(pattern, phone_number)


@frappe.whitelist(allow_guest=True)
def validateOTP(**kwargs):
    global otp
    global phone_number

    recOTP = kwargs.get("myOTP")
    recNUM = kwargs.get("phone_number")
    if (recOTP == otp) and (recNUM == phone_number):
        return {
            "status": "success",
            "message": "OTP is correct.",
        }

    else:
        return {
            "status": "fail",
            "message": "OTP is incorrect.",
        }
