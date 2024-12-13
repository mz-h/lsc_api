// Copyright (c) 2024, M and contributors
// For license information, please see license.txt

frappe.ui.form.on('Client Transaction', {
    refresh: function (frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Task'), function () {
                frappe.model.open_mapped_doc({
                    method: "lsc_api.lsc_api.doctype.client_transaction.client_transaction.create_task",
                    frm: frm
                });
            });
        }
    }
});

