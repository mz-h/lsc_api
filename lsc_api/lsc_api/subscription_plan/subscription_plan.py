import frappe
from frappe import _
import requests

from lsc_api.utils.error_handler import handle_error
from lsc_api.utils.jwt import verify_jwt_middleware


@frappe.whitelist(methods=["GET"])
def get_subscription_status():
    # Get the current authenticated user
    user = frappe.session.user

    # Get customer
    customer = frappe.get_list(
        "Customer", filters={"custom_user": user}, limit=1, fields=["name"]
    )
    if not customer:
        return {"data": {"message": "This user has no customer doc"}}

    customer = customer[0]
    subscription_id = frappe.db.exists(
        "Subscription", {"status": "Active", "party": customer.name}
    )

    if subscription_id:
        subscription = frappe.get_doc(
            "Subscription", {"name": subscription_id, "status": "Active"}
        )
        subscription_plan_id = subscription.plans[0]

        subscription_plan = frappe.get_doc(
            "Subscription Plan", subscription_plan_id.plan
        )

        quota = frappe.get_all(
            "Quota", {"parent": subscription_id, "parentfield": "custom_quota"}, "*"
        )

        remaining_cons = 0
        remaining_cases = 0
        remaining_legals = 0

        for row in quota:
            if row.service_name == "ساعات الاستشارة":
                remaining_cons = row.hrs
            elif row.service_name == "ساعات الخدمات القانونية":
                remaining_legals = row.hrs
            elif row.service_name == "ساعات القضايا":
                remaining_cases = row.hrs

        # return subscription_plan
        total_hours = (
            int(subscription_plan.custom_total_hrs)
            + int(subscription_plan.custom_total_hrs_cases)
            + int(subscription_plan.custom_total_hrs_legal_services)
        )

        allowed_services = [
            r.service_name for r in subscription_plan.custom_allowed_services
        ]
        remaining_hours = 0
        for r in subscription.custom_quota:
            remaining_hours += int(r.hrs)

        return {
            "data": {
                "subscription": {
                    "subscription_plan": subscription_plan.name,
                    "plan_fees": subscription_plan.cost,
                    "status": subscription.status,
                    "invoice_start_date": subscription.current_invoice_start,
                    "invoice_end_date": subscription.current_invoice_end,
                    "consultation_hrs": subscription_plan.custom_total_hrs,
                    "remaining_consultation_hrs": remaining_cons,
                    "cases_hrs": subscription_plan.custom_total_hrs_cases,
                    "remaining_cases_hrs": remaining_cases,
                    "legal_services_hrs": subscription_plan.custom_total_hrs_legal_services,
                    "remaining_legal_services_hrs": remaining_legals,
                    "total_hours": total_hours,
                    "remaining_hours": remaining_hours,
                    "allowed_services": allowed_services,
                }
            }
        }

    return {"data": {"subscription": None}}


@frappe.whitelist(methods=["GET"])
def get_subscriptions():
    try:
        params = frappe.local.request.args
        # Convert parameters to integers
        try:
            page = params.get("page")
            size = params.get("size")

            page = int(page) if page else 1
            size = int(size) if size else 5
        except ValueError:
            return handle_error("Page number and page length should be integers")

        limit_start = (page - 1) * size

        # Fetch the list of subscription plans with their allowed services
        plans = frappe.get_all(
            "Subscription Plan",
            fields=[
                "name",
                "plan_name",
                "currency",
                "cost",
                "billing_interval",
                "billing_interval_count",
                "cost_center",
                "custom_total_hrs",
                "custom_total_hrs_cases",
                "custom_total_hrs_legal_services",
                "custom_total_plan_hrs",
            ],
            order_by="cost desc",
            # limit_start=limit_start,
            # limit_page_length=size,
        )

        # For each plan, fetch the associated allowed services
        for plan in plans:
            plan_items = frappe.get_all(
                "Allowed Service",
                fields=["service_name"],
                filters={"parent": plan["name"]},
            )
            plan["allowed_services"] = plan_items

        return {"message": "success", "length": len(plans), "data": plans}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error fetching subscription plans"))
        return {"error": str(e)}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def create_subscription(**kwargs):
    try:
        # Get the current authenticated user
        user = frappe.session.user

        data = kwargs.get("data")
        plan_name = data.get("plan_name")

        # Validate the input parameters (plan_name, start_date, end_date)
        if not plan_name:
            return {"status": "error", "message": _("plan_name field is required.")}

        # Fetch the Subscription Plan to ensure it exists
        plan = frappe.get_doc("Subscription Plan", plan_name)
        if not plan:
            return {"error": _("The subscription plan does not exist.")}

        # Get customer
        customer = frappe.get_list("Customer", filters={"custom_user": user}, limit=1)
        if not customer:
            return {"status": "fail", "message": _("This user has no customer.")}

        customer = customer[0]

        # subscription_id = frappe.db.exists("Subscription", {"status": "Unpaid", "party": customer.name})
        # if subscription_id:
        #     if frappe.db.exists("Subscription Plan Detail", {"parent":subscription_id, "plan": plan.name }):
        #         subscription = frappe.get_doc("Subscription", {"status": "Unpaid", "party": customer.name})

        #         return {
        #             "status": "success",
        #             "message": _("Subscription is already created successfully, Complete the payment process."),
        #             "data": {
        #                 "sales_invoice": subscription.custom_sales_invoice
        #             },
        #         }

        # Create the Subscription entry
        subscription = frappe.get_doc(
            {
                "doctype": "Subscription",
                "party_type": "Customer",
                "party": customer.name,
                "company": "LSC",
                "status": "Unpaid",
                "days_until_due": 5,
                "generate_invoice_at": "Beginning of the current subscription period",
                "generate_new_invoices_past_due_date": 1,
                "submit_invoice": 1,
                "sales_tax_template": "KSA VAT 15% - LSC",
                # "start_date": start_date, # paid day
                # "end_date": end_date, # paid day plus based on the interval of subscription plan
            }
        )

        # Add child table plans {plan, qty}
        subscription.append(
            "plans",
            {
                "plan": plan.name,
                "qty": 1,
            },
        )

        subscription.insert(ignore_permissions=True)
        subscription.status = "Unpaid"
        subscription.save(ignore_permissions=True)

        if frappe.db.exists("Sales Invoice", subscription.custom_sales_invoice):
            sales_inv = frappe.get_doc(
                "Sales Invoice", subscription.custom_sales_invoice
            )
        else:
            return {
                "status": "fail",
                "message": _("Subscription created but cannot find invoice."),
            }

        return {
            "status": "success",
            "message": _("Subscription created successfully."),
            "data": {"sales_invoice": sales_inv.name},
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error creating subscription"))
        return {"error": str(e)}


@frappe.whitelist(methods=["POST"])
def pay_subscription(**kwargs):
    try:
        # Get the current authenticated user
        user = frappe.session.user
        user_data = frappe.get_all(
            "User",
            filters={"name": user},
            fields=["first_name", "middle_name", "last_name", "phone"],
            limit=1,
        )
        if not user_data:
            return {"status": "fail", "message": "User not found"}
        user_data = user_data[0]

        # Get data from kwargs
        data = kwargs.get("data")
        sales_invoice = data.get("sales_invoice")
        save_card = data.get("save_card")

        if not sales_invoice:
            return {"status": "fail", "message": "Sales invoice not provided"}

        # Check if Sales Invoice exists
        if not frappe.db.exists("Sales Invoice", {"name": sales_invoice}):
            return {
                "status": "fail",
                "message": f"This sales invoice {sales_invoice} is not found",
            }

        if frappe.db.exists("Sales Invoice", {"name": sales_invoice, "status": "Paid"}):
            return {
                "status": "fail",
                "message": f"This sales invoice {sales_invoice} is already Paid",
            }

        try:
            # Fetch the Subscription linked to the sales invoice
            subscription = frappe.get_doc(
                "Subscription", {"custom_sales_invoice": sales_invoice}
            )

            # Get the subscription plan details
            subscription_plan = frappe.get_all(
                "Subscription Plan",
                filters={"name": subscription.plans[0].plan},
                fields=["cost", "name", "currency"],
                limit=1,
            )
            if not subscription_plan:
                return {"status": "fail", "message": "Subscription plan not found"}
            subscription_plan = subscription_plan[0]

            # Payment API request
            url = "https://api.tap.company/v2/charges"
            headers = {
                "Authorization": "Bearer sk_test_HZRGImxq8Euzi1b4h2AB7Kks",
                "Content-Type": "application/json",
            }

            payment_data = {
                "amount": subscription_plan.cost,
                "currency": subscription_plan.currency,  # or the currency you're using
                "customer_initiated": True,
                "threeDSecure": True,
                "save_card": False,
                # "save_card": True,
                # "save_card": save_card if save_card else False,
                "description": subscription_plan.name,
                "receipt": {
                    "email": True,
                    "sms": True,
                },
                "metadata": {
                    "sales_invoice": sales_invoice,
                    "custom_status": "pending_payment",  # Custom metadata passed to redirect URL
                },
                "customer": {
                    "first_name": user_data.get("first_name"),
                    "middle_name": user_data.get(
                        "middle_name", user_data.get("first_name")
                    ),
                    "last_name": user_data.get("last_name"),
                    "email": user,
                    "phone": {"number": user_data.get("phone")},
                },
                "source": {
                    "id": "src_all"  # Indicate that all sources (like cards) are allowed
                },
                "post": {
                    "url": "https://lsc.psc-s.com/api/method/lsc_api.lsc_api.subscription_plan.subscription_plan.tap_handler"
                },
                "redirect": {
                    "url": "https://lsc.psc-s.com/dashboard/profile/payRes"  # Redirect URL after payment completion
                },
            }

            try:
                # Make the payment request
                response = requests.post(url, headers=headers, json=payment_data)
                # response.raise_for_status()  # Raise exception for HTTP errors
                response_data = response.json()

                # Update the subscription with the tap charge ID
                subscription.custom_tap_charge_id = response_data["id"]
                subscription.save(ignore_permissions=True)

                return {
                    "status": "success",
                    "CALLER": "OMAR",
                    "data": {"transaction": response_data["transaction"]},
                }
            except:
                return {
                    "status": "fail",
                    "message": "Fail to create checkout url",
                }

        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Payment API error: {str(e)}"}
        except frappe.DoesNotExistError:
            return {"status": "fail", "message": "Subscription not found"}
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), _("Payment FAILED"))
            return {
                "status": "fail",
                "message": "Something is wrong",
            }

    except frappe.DoesNotExistError:
        return {"status": "fail", "message": "User not found"}
    except Exception as e:
        return {"status": "fail", "message": f"An unexpected error occurred: {str(e)}"}


@frappe.whitelist(allow_guest=True)
def tap_handler(**kwargs):
    try:
        frappe.set_user("Administrator")

        data = frappe.request.json
        frappe.log_error(frappe.as_json(data), "Tap Webhook Response")
        payment_status = data.get("status")

        sales_invoice_name = data.get("metadata").get("sales_invoice")

        if not sales_invoice_name:
            frappe.log_error("No reference ID found in Tap webhook data")
            return

        transaction = data.get("transaction", {})
        transaction_amount = transaction.get("amount")

        if not transaction_amount:
            frappe.log_error("Transaction amount is missing")
            return

        if payment_status == "CAPTURED":
            try:
                sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)
            except frappe.DoesNotExistError:
                frappe.log_error(f"Sales Invoice {sales_invoice_name} does not exist")
                return
            company_settings = frappe.get_doc("Company", "LSC")
            payment_entry_data = {
                "doctype": "Payment Entry",
                "payment_type": "Receive",
                "party_type": "Customer",
                "party": sales_invoice.customer,
                "posting_date": frappe.utils.nowdate(),
                "mode_of_payment": "نقد",  # Set to the appropriate mode of payment
                "paid_from": company_settings.default_receivable_account,
                "paid_to": company_settings.default_cash_account,
                "paid_amount": transaction_amount,
                "received_amount": transaction_amount,
                "references": [
                    {
                        "reference_doctype": "Sales Invoice",
                        "reference_name": sales_invoice.name,
                        "allocated_amount": transaction_amount,
                        "account": company_settings.default_receivable_account,
                    }
                ],
                "remarks": f"Payment against Sales Invoice: {sales_invoice.name}",
            }

            payment_entry = frappe.get_doc(payment_entry_data)
            payment_entry.insert(ignore_permissions=True)
            payment_entry.submit()

            # Set subscription to active if applicable
            subscription = frappe.get_doc(
                "Subscription", {"custom_sales_invoice": sales_invoice.name}
            )
            subscription.status = "Active"
            subscription.save(ignore_permissions=True)

            #  Cancel previous subscriptions
            customer_subscriptions = frappe.get_all(
                "Subscription",
                filters={
                    "party": sales_invoice.customer,
                    "status": "Active",
                    "name": ["!=", subscription.name],
                },
                fields=["name"],
            )

            for subscription in customer_subscriptions:
                old_subscription = frappe.get_doc(
                    "Subscription", subscription.get("name")
                )
                old_subscription.status = "Cancelled"
                old_subscription.save(ignore_permissions=True)

            return {"status": "success", "redirect": "https://lsc.psc-s.com/success"}
        elif payment_status == "FAILED":
            frappe.log_error(f"Payment failed for Sales Invoice {sales_invoice_name}")
            return {"status": "fail", "redirect": "https://lsc.psc-s.com/failure"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Payment Initiation Failed"))
        return {"status": "error", "redirect": "https://lsc.psc-s.com/failure"}

    # data = frappe.request.json
    # return data

    # # Get the current authenticated user
    # user = frappe.session.user

    # customer = frappe.get_doc("Customer", {"custom_user": user})

    # data = kwargs.get('data')
    # sales_invoice = data.get('sales_invoice')

    # # Check if the sales invoice exists and is not already submitted
    # if frappe.db.exists("Sales Invoice", sales_invoice):
    #     sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice)

    #     if sales_invoice_doc.customer != customer.name:
    #         return {"status": "fail", "message": "Forbidden"}

    #     # Activate Subscription
    #     if frappe.db.exists("Subscription", {"custom_sales_invoice": sales_invoice}):
    #         subscription = frappe.get_doc("Subscription", {"custom_sales_invoice": sales_invoice})

    #         url = f"https://api.tap.company/v2/charges/{subscription.custom_tap_charge_id}"
    #         headers = {
    #             "Authorization": "Bearer sk_test_6RfmheuSW2zlVtvBdOCUEM4c",
    #             "Content-Type": "application/json"
    #         }

    #         response = requests.post(url, headers=headers, json=data)
    #         response_data = response.json()

    #         return response_data

    #         if response_data['status'] == 'CAPTURED':

    #             subscription.status = 'Active'
    #             subscription.save()

    #             if sales_invoice_doc.docstatus == 0:
    #                 # Submit the Sales Invoice
    #                 sales_invoice_doc.submit()

    #             # Create Payment Entry for the Sales Invoice
    #             payment_entry = frappe.new_doc("Payment Entry")
    #             payment_entry.payment_type = "Receive"
    #             payment_entry.party_type = "Customer"
    #             payment_entry.party = sales_invoice_doc.customer
    #             payment_entry.party_name = sales_invoice_doc.customer
    #             payment_entry.posting_date = frappe.utils.nowdate()
    #             # payment_entry.mode_of_payment = "Tap Payment"  # Replace with your mode of payment
    #             payment_entry.paid_amount = sales_invoice_doc.outstanding_amount
    #             payment_entry.paid_to = '1110 - النقدية في الخزينة - LSC'
    #             payment_entry.paid_to_account_currency = sales_invoice_doc.currency
    #             # payment_entry.received_amount = sales_invoice_doc.outstanding_amount
    #             payment_entry.reference_no = "Tap_Payment_" + subscription.custom_tap_charge_id  # Replace with actual reference from Tap
    #             payment_entry.reference_date = frappe.utils.nowdate()
    #             payment_entry.append("references", {
    #                 "reference_doctype": "Sales Invoice",
    #                 "reference_name": sales_invoice_doc.name,
    #                 "total_amount": sales_invoice_doc.grand_total,
    #                 "outstanding_amount": sales_invoice_doc.outstanding_amount,
    #                 "allocated_amount": sales_invoice_doc.outstanding_amount,
    #             })

    #             payment_entry.insert()
    #             payment_entry.submit()

    #             return {
    #                 "status": "success",
    #                 "message": f"Payment confirmed, Sales Invoice {sales_invoice} submitted, Payment Entry {payment_entry.name} created, and Subscription activated."
    #             }

    #         else:
    #             return {
    #                 "status": "fail",
    #                 "message": "Failed Payment Process"
    #             }
    # else:
    #     return {
    #         "status": "fail",
    #         "message": f"This sales invoice {sales_invoice} is not found."
    #     }


# @frappe.whitelist(allow_guest=True)
# def initiate_subscription_and_redirect(customer_id, subscription_plan, payment_details):
#     try:
#         # Step 1: Validate the customer and subscription plan
#         customer = frappe.get_doc("Customer", customer_id)
#         plan = frappe.get_doc("Subscription Plan", subscription_plan)

#         if not customer or not plan:
#             frappe.throw(_("Invalid Customer or Subscription Plan"))

#         # Step 2: Initiate the payment process using Tap payment gateway
#         payment_response = initiate_tap_payment(payment_details)

#         if payment_response.get("status") != "INITIATED":
#             frappe.throw(_("Payment initiation failed"))

#         # Step 3: Redirect to the transaction URL
#         transaction_url = payment_response.get("transaction", {}).get("url")
#         if not transaction_url:
#             frappe.throw(_("Transaction URL not found in the payment response"))

#         # Perform the redirect
#         frappe.local.response["type"] = "redirect"
#         frappe.local.response["location"] = transaction_url

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Payment Initiation Failed"))
#         frappe.throw(_("An error occurred: {0}").format(str(e)))
