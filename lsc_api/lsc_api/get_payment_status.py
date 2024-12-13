import frappe
from frappe import _
import requests

@frappe.whitelist(allow_guest=True)
def get_payment_status(**kwargs):

    try:
        params = frappe.local.request.args
        charge_id = params.get("id")

        # Payment API request
        url = "https://api.tap.company/v2/charges"
        headers = {
            "Authorization": "Bearer sk_test_HZRGImxq8Euzi1b4h2AB7Kks",
            "Content-Type": "application/json",
        }

        response = requests.get(f'{url}/{charge_id}', headers=headers)

        data = response.json()

        return { "status": data.get('status') }

    except:
        return {"status": "fail", "message": "Something was wrong"}

