from frappe.model.document import Document

from collections.abc import Iterable

import frappe
from frappe import _
from frappe.cache_manager import clear_doctype_map, get_doctype_map
from frappe.desk.form import assign_to
from frappe.model import log_types
from frappe.model.document import Document
from frappe.utils.data import comma_and


class AssignByRole(Document):
    
    def validate(self):
        self.validate_document_types()
        self.validate_assignment_days()

    def clear_cache(self):
        super().clear_cache()
        clear_doctype_map(self.doctype, self.document_type)
        clear_doctype_map(self.doctype, f"due_date_rules_for_{self.document_type}")

    def validate_document_types(self):
        if self.document_type == "ToDo":
            frappe.throw(_("Assign By Role is not allowed on {0} document type").format(frappe.bold("ToDo")))

    def validate_assignment_days(self):
        assignment_days = self.get_assignment_days()
        if len(set(assignment_days)) != len(assignment_days):
            frappe.throw(
                _("The following Assignment Days have been repeated: {0}").format(
                    comma_and([_(day) for day in get_repeated(assignment_days)], add_quotes=False)
                )
            )

    def apply_unassign(self, doc, assignments):
        if self.unassign_condition and self.name in [d.custom_asign_by_role for d in assignments]:
            return self.clear_assignment(doc)

        return False

    def apply_assign(self, doc):
        if self.safe_eval("assign_condition", doc):
            return self.do_assignment(doc)

    def do_assignment(self, doc):
        # clear existing assignment, to reassign
        # assign_to.clear(doc.get("doctype"), doc.get("name"), ignore_permissions=True)

        user = self.get_user(doc)

        if user:
            assign_to.add(
                dict(
                    assign_to=[user],
                    doctype=doc.get("doctype"),
                    name=doc.get("name"),
                    description=frappe.render_template(self.description, doc),
                    custom_asign_by_role=self.name,
                    notify=True,
                    date=doc.get(self.due_date_based_on) if self.due_date_based_on else None,
                ),
                ignore_permissions=True,
            )
            ## assign to client transaction
            if doc.get("doctype") in ["Case", "Cases Study", "Legal Service", "Consultation"]:
                assign_to.add(
                    dict(
                        assign_to=[user],
                        doctype="Client Transaction",
                        name=doc.get("client_transaction"),
                        description=frappe.render_template(self.description, doc),
                        custom_asign_by_role=self.name,
                        notify=True,
                        date=doc.get(self.due_date_based_on) if self.due_date_based_on else None,
                    ),
                    ignore_permissions=True,
                )
            

            # set for reference in round robin
            self.db_set("last_user", user)
            return True

        return False

    def clear_assignment(self, doc):
        """Clear assignments"""
        if self.safe_eval("unassign_condition", doc):
            return assign_to.clear(doc.get("doctype"), doc.get("name"), ignore_permissions=True)

    def close_assignments(self, doc):
        """Close assignments"""
        if self.safe_eval("close_condition", doc):
            return assign_to.close_all_assignments(
                doc.get("doctype"), doc.get("name"), ignore_permissions=True
            )

    def get_user(self, doc):
        return self.get_user_load_balancing(self.role)

    def get_user_round_robin(self):
        """
        Get next user based on round robin
        """

        # first time, or last in list, pick the first
        if not self.last_user or self.last_user == self.users[-1].user:
            return self.users[0].user

        # find out the next user in the list
        for i, d in enumerate(self.users):
            if self.last_user == d.user:
                return self.users[i + 1].user

        # bad last user, assign to the first one
        return self.users[0].user

    def get_user_load_balancing(self, designation):
        """Assign to the user with the least number of open assignments based on role"""
        
        # Get users with the specified role
        filters = {'designation': designation}
        if self.branch:
            filters.update({"branch":self.branch})
        users = frappe.get_all('Employee', filters=filters, fields=['user_id'])
        user_list = [user['user_id'] for user in users]

        if not user_list:
            frappe.throw(f"No users found for the role: {designation}")

        # Calculate the number of open assignments (ToDo) for each user
        counts = [
            dict(
                user=user,
                count=frappe.db.count(
                    "ToDo",
                    dict(
                        reference_type=self.document_type,
                        allocated_to=user,
                        status="Open",
                    ),
                ),
            )
            for user in user_list
        ]

        # Sort by the count of open assignments
        sorted_counts = sorted(counts, key=lambda k: k["count"])

        # Return the user with the least number of open assignments
        return sorted_counts[0]["user"] if sorted_counts else None


    def get_user_based_on_field(self, doc):
        val = doc.get(self.field)
        if frappe.db.exists("User", val):
            return val

    def safe_eval(self, fieldname, doc):
        try:
            if self.get(fieldname):
                return frappe.safe_eval(self.get(fieldname), None, doc)
        except Exception as e:
            # when assignment fails, don't block the document as it may be
            # a part of the email pulling
            frappe.msgprint(frappe._("Auto assignment failed: {0}").format(str(e)), indicator="orange")

        return False

    def get_assignment_days(self):
        return [d.day for d in self.get("assignment_days", [])]

    def is_rule_not_applicable_today(self):
        today = frappe.flags.assignment_day or frappe.utils.get_weekday()
        assignment_days = self.get_assignment_days()
        return assignment_days and today not in assignment_days


def get_assignments(doc) -> list[dict]:
    return frappe.get_all(
        "ToDo",
        fields=["name", "custom_asign_by_role"],
        filters=dict(
            reference_type=doc.get("doctype"), reference_name=doc.get("name"), status=("!=", "Cancelled")
        ),
        limit=5,
    )


@frappe.whitelist()
def bulk_apply(doctype, docnames):
    docnames = frappe.parse_json(docnames)
    background = len(docnames) > 5

    for name in docnames:
        if background:
            frappe.enqueue(
                "frappe.automation.doctype.assignment_rule.assignment_rule.apply",
                doc=None,
                doctype=doctype,
                name=name,
            )
        else:
            apply(doctype=doctype, name=name)


def reopen_closed_assignment(doc):
    todo_list = frappe.get_all(
        "ToDo",
        filters={
            "reference_type": doc.doctype,
            "reference_name": doc.name,
            "status": "Closed",
        },
        pluck="name",
    )

    for todo in todo_list:
        todo_doc = frappe.get_doc("ToDo", todo)
        todo_doc.status = "Open"
        todo_doc.save(ignore_permissions=True)

    return bool(todo_list)


def apply(doc=None, method=None, doctype=None, name=None):
    try:
        doctype = doctype or (doc and doc.doctype)

        # Skip assignment rules if in specific states or log_types
        skip_assignment_rules = (
            frappe.flags.in_patch
            or frappe.flags.in_install
            or frappe.flags.in_setup_wizard
            or doctype in log_types
        )

        if skip_assignment_rules:
            return

        # Fetch the document if not provided
        if not doc and doctype and name:
            if frappe.db.exists(doctype, name):
                doc = frappe.get_doc(doctype, name)
                frappe.log_error(message=f"Document fetched: {doc.name}", title="Debug Log")
            else:
                frappe.log_error(message=f"Document {doctype} {name} not found.", title="Debug Log")
                return  # Document not found

        if doc:
            # Fetch applicable assignment rules
            assignment_rules = get_doctype_map(
                "Assign By Role",
                doc.doctype,
                filters={"document_type": doc.doctype, "disabled": 0},
                order_by="priority desc",
            )

            if not assignment_rules:
                return  # No rules to apply

            # Load rule documents
            assignment_rule_docs = [
                frappe.get_cached_doc("Assign By Role", rule.get("name")) for rule in assignment_rules
            ]

            doc_dict = doc.as_dict()
            assignments = get_assignments(doc_dict)

            clear = True  # Indicates whether all assignments are cleared
            new_apply = False  # Tracks if new assignments were applied

            # Unassign existing assignments if applicable
            # for assignment_rule in assignment_rule_docs:
            #     if assignment_rule.is_rule_not_applicable_today():
            #         continue

            #     clear = assignment_rule.apply_unassign(doc_dict, assignments)
            #     if clear:
            #         break

            # Apply new assignments if all are cleared
            if clear:
                for assignment_rule in assignment_rule_docs:
                    if assignment_rule.is_rule_not_applicable_today():
                        continue

                    new_apply = assignment_rule.apply_assign(doc_dict)

                    if new_apply:
                        break  # Stop after applying the first rule
            
            if not new_apply:
                frappe.log_error(
                    message=f"No assignment could be made for {doc.doctype} {doc.name}.",
                    title="Assignment Failure",
                )

            # Check and handle closing assignments
            assignments = get_assignments(doc_dict)
            if assignments:
                for assignment_rule in assignment_rule_docs:
                    if assignment_rule.is_rule_not_applicable_today():
                        continue

                    # Evaluate close condition
                    to_close_todos = assignment_rule.safe_eval("close_condition", doc_dict)
                    if to_close_todos:
                        # Close relevant todos
                        todos_to_close = frappe.get_all(
                            "ToDo",
                            filters={
                                "reference_type": doc.doctype,
                                "reference_name": doc.name,
                            },
                            pluck="name",
                        )

                        for todo_name in todos_to_close:
                            todo_doc = frappe.get_doc("ToDo", todo_name)
                            todo_doc.status = "Closed"
                            todo_doc.save(ignore_permissions=True)
                        break
                    else:
                        # Reopen closed assignments if needed
                        if reopen_closed_assignment(doc_dict):
                            break

                    assignment_rule.close_assignments(doc_dict)
    except Exception as e:
        # Log the error with context for debugging
        frappe.log_error(
            message=frappe.get_traceback(),
            title=f"Error in Apply Function: {doctype or 'Unknown Doctype'}",
        )


def update_due_date(doc, state=None):
    """Run on_update on every Document (via hooks.py)"""
    skip_document_update = (
        frappe.flags.in_migrate
        or frappe.flags.in_patch
        or frappe.flags.in_import
        or frappe.flags.in_setup_wizard
        or frappe.flags.in_install
    )

    if skip_document_update:
        return

    assignment_rules = get_doctype_map(
        doctype="Assign By Role",
        name=f"due_date_rules_for_{doc.doctype}",
        filters={
            "due_date_based_on": ["is", "set"],
            "document_type": doc.doctype,
            "disabled": 0,
        },
    )

    for rule in assignment_rules:
        rule_doc = frappe.get_cached_doc("Assign By Role", rule.get("name"))
        due_date_field = rule_doc.due_date_based_on
        field_updated = (
            doc.meta.has_field(due_date_field) and doc.has_value_changed(due_date_field) and rule.get("name")
        )

        if field_updated:
            assignment_todos = frappe.get_all(
                "ToDo",
                filters={
                    "custom_asign_by_role": rule.get("name"),
                    "reference_type": doc.doctype,
                    "reference_name": doc.name,
                    "status": "Open",
                },
                pluck="name",
            )

            for todo in assignment_todos:
                todo_doc = frappe.get_doc("ToDo", todo)
                todo_doc.date = doc.get(due_date_field)
                todo_doc.flags.updater_reference = {
                    "doctype": "Assign By Role",
                    "docname": rule.get("name"),
                    "label": _("via Assign By Role"),
                }
                todo_doc.save(ignore_permissions=True)


def get_assignment_rules() -> list[str]:
    return frappe.get_all("Assign By Role", filters={"disabled": 0}, pluck="document_type")


def get_repeated(values: Iterable) -> list:
    unique = set()
    repeated = set()

    for value in values:
        if value in unique:
            repeated.add(value)
        else:
            unique.add(value)

    return [str(x) for x in repeated]