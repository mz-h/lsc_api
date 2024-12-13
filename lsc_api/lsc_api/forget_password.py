import frappe


@frappe.whitelist(allow_guest=True)
def verify_mobile(**kwargs):
    mobile_no = kwargs.get("mobile_no")
    if not mobile_no:
        return {"status": "fail", "message": "Mobile number is required."}

    user = frappe.db.get_value("User", {"mobile_no": mobile_no}, "email")

    if user:
        return {"status": "success", "email": user}
    else:
        return {"status": "fail", "message": "No user found with this mobile number."}


@frappe.whitelist(allow_guest=True)
def reset_password(**kwargs):
    new_password = kwargs.get("new_password")
    email = kwargs.get("email")

    if not email or not new_password:
        return {"status": "fail", "message": "Email and new password are required."}

    user = frappe.get_doc("User", {"email": email})

    if user:
        try:
            update_password(user, new_password)
            return {"status": "success", "message": "Password updated successfully."}
        except Exception as e:
            return {"status": "fail", "message": f"Error updating password: {str(e)}"}
    else:
        return {"status": "fail", "message": "No user found with this email."}
