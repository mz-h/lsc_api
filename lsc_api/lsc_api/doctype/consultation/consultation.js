frappe.ui.form.on('Consultation', {
    onload: function (frm) {
        // Initialize the fields with default values if empty
        if (!frm.doc.end_time) {
            frm.set_value('end_time', '12:00 AM');
        }
        if (!frm.doc.start_time) {
            frm.set_value('start_time', '12:00 AM');
        }
    },
    refresh: function (frm) {
        frm.add_custom_button(__('Re Assign'), function () {
            let d = new frappe.ui.Dialog({
                title: 'Insert Employee',
                fields: [
                    {
                        label: 'Employee',
                        fieldname: 'employee',
                        fieldtype: 'Link',
                        options: "Employee",
                        reqd: 1
                    }
                ],
                primary_action_label: 'Set Employee',
                primary_action({ employee }) {
                    frappe.call({
                        method: 'set_employee',
                        doc: frm.doc,
                        args: {
                            employee
                        },
                        callback: function (response) {
                            console.log(response)
                            if (!response.exc) {
                                frm.reload_doc();
                            }
                        }
                    });
                    d.hide();
                }
            });

            d.show();
        });

        frm.add_custom_button(__('Add Link to Comments'), function () {
            let d = new frappe.ui.Dialog({
                title: 'Insert Link',
                fields: [
                    {
                        label: 'Use Fixed Link',
                        fieldname: 'use_custom_link',
                        fieldtype: 'Check',
                        description: 'Check to enter a custom link',
                        reqd: 0
                    },
                    {
                        label: 'Label',
                        fieldname: 'label',
                        fieldtype: 'Data',
                        description: 'Insert label (e.g., here is the meeting link!)',
                        reqd: 0
                    },
                    {
                        label: 'Link',
                        fieldname: 'link',
                        fieldtype: 'Data',
                        description: 'Insert link (e.g., http://meet.google.com)',
                        reqd: 0,
                        depends_on: 'eval: doc.use_custom_link == 0'
                    },
                    {
                        label: 'Fixed Link',
                        fieldname: 'custom_link',
                        fieldtype: 'Link',
                        options: 'Fixed Comment Links',
                        description: 'Select a predefined link..',
                        depends_on: 'eval: doc.use_custom_link == 1',
                        reqd: 0
                    },
                    {
                        label: 'New tab?',
                        fieldname: 'new_tab',
                        fieldtype: 'Check',
                        reqd: 0
                    },
                ],
                primary_action_label: 'Insert',
                primary_action(values) {
                    let comment;

                    if (values.use_custom_link) {
                        if (values.use_custom_link && values.custom_link) {
                            frappe.call({
                                method: 'frappe.client.get',
                                args: {
                                    doctype: 'Fixed Comment Links',
                                    name: values.custom_link
                                },
                                callback: function (r) {
                                    if (r.message) {
                                        let custom_link_value = r.message.link;

                                        comment = `label:${values.label} || tab: ${values.new_tab} || link:${custom_link_value}`;
                                        frappe.call({
                                            method: 'frappe.client.insert',
                                            args: {
                                                doc: {
                                                    doctype: 'Comment',
                                                    comment_type: 'Comment',
                                                    reference_doctype: frm.doctype,
                                                    reference_name: frm.docname,
                                                    content: comment
                                                }
                                            },
                                            callback: function (response) {
                                                if (!response.exc) {
                                                    frm.reload_doc();
                                                }
                                            }
                                        });
                                        d.hide();
                                    }
                                }
                            });
                        }
                    } else {
                        comment = `label:${values.label} || tab: ${values.new_tab} || link:${values.link}`;
                        frappe.call({
                            method: 'frappe.client.insert',
                            args: {
                                doc: {
                                    doctype: 'Comment',
                                    comment_type: 'Comment',
                                    reference_doctype: frm.doctype,
                                    reference_name: frm.docname,
                                    content: comment
                                }
                            },
                            callback: function (response) {
                                if (!response.exc) {
                                    frm.reload_doc();
                                }
                            }
                        });
                        d.hide();
                    }
                }
            });

            d.show();
        });

        // Add event listener for input changes
        frm.fields_dict.end_time.$input.on('change', function () {
            updateTimeAMPM(frm, 'end_time');
        });
        frm.fields_dict.start_time.$input.on('change', function () {
            updateTimeAMPM(frm, 'start_time');
        });

        // Add event listener for focus to show time picker
        frm.fields_dict.end_time.$input.on('focus', function () {
            showTimePicker(frm, 'end_time');
        });
        frm.fields_dict.start_time.$input.on('focus', function () {
            showTimePicker(frm, 'start_time');
        });
    }
});

// Function to update the time in AM/PM format
function updateTimeAMPM(frm, fieldname) {
    let time_val = frm.doc[fieldname];
    if (time_val) {
        let time_regex = /^(\d{1,2}):(\d{2})(?:\s?(AM|PM))?$/i;
        let match = time_val.match(time_regex);

        if (match) {
            let hours = parseInt(match[1]);
            let minutes = match[2];
            let ampm = match[3];

            if (!ampm) {
                ampm = hours >= 12 ? 'PM' : 'AM';
                hours = hours % 12;
                hours = hours ? hours : 12; // the hour '0' should be '12'
            } else {
                ampm = ampm.toUpperCase();
                if (ampm === 'PM' && hours < 12) {
                    hours += 12;
                } else if (ampm === 'AM' && hours === 12) {
                    hours = 0;
                }
            }

            let strTime = hours.toString().padStart(2, '0') + ':' + minutes.padStart(2, '0') + ' ' + ampm;
            frm.set_value(fieldname, strTime);
        } else {
            frappe.msgprint(__('Please enter time in HH:MM format.'));
        }
    }
}

// Function to show a custom time picker
function showTimePicker(frm, fieldname) {
    let time_val = frm.doc[fieldname];
    let [hours, minutes, ampm] = [12, '00', 'AM'];

    if (time_val) {
        let time_regex = /^(\d{1,2}):(\d{2})\s?(AM|PM)$/i;
        let match = time_val.match(time_regex);
        if (match) {
            hours = parseInt(match[1]);
            minutes = match[2];
            ampm = match[3].toUpperCase();
        }
    }

    let timePickerHtml = `
        <div class="time-picker">
            <input type="number" class="time-picker-hours form-control ellipsis bold mr-2" value="${hours}" min="1" max="12" style="min-width: max-content;">
            :
            <input type="number" class="time-picker-minutes form-control ellipsis bold mx-2" value="${minutes}" min="0" max="59" style="min-width: max-content;">
            <select class="time-picker-ampm form-control ellipsis bold">
                <option value="AM" ${ampm === 'AM' ? 'selected' : ''}>AM</option>
                <option value="PM" ${ampm === 'PM' ? 'selected' : ''}>PM</option>
            </select>
            <button class="time-picker-set btn btn-xs btn-secondary grid-add-row ml-2">Set</button>
        </div>
    `;

    let timePicker = $(timePickerHtml).appendTo('body');
    timePicker.css({
        position: 'absolute',
        top: frm.fields_dict[fieldname].$input.offset().top + frm.fields_dict[fieldname].$input.outerHeight(),
        left: frm.fields_dict[fieldname].$input.offset().left,
        zIndex: 1000,
        background: '#fff',
        border: '1px solid #ddd',
        padding: '10px',
        borderRadius: '4px',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        display: 'flex'
    });

    timePicker.find('.time-picker-hours').on('input', function () {
        let value = parseInt($(this).val());
        if (value > 12) {
            $(this).val(12);
        } else if (value < 1) {
            $(this).val(1);
        }
    });

    timePicker.find('.time-picker-minutes').on('input', function () {
        let value = parseInt($(this).val());
        if (value > 59) {
            $(this).val(59);
        } else if (value < 0) {
            $(this).val(0);
        }
    });

    timePicker.find('.time-picker-set').on('click', function () {
        let selectedHours = parseInt(timePicker.find('.time-picker-hours').val());
        let selectedMinutes = timePicker.find('.time-picker-minutes').val().padStart(2, '0');
        let selectedAmPm = timePicker.find('.time-picker-ampm').val();
        let formattedTime = selectedHours + ':' + selectedMinutes + ' ' + selectedAmPm;
        frm.set_value(fieldname, formattedTime);
        timePicker.remove();
    });

    $(document).on('click', function (event) {
        if (!$(event.target).closest('.time-picker').length && !$(event.target).closest(frm.fields_dict[fieldname].$input).length) {
            timePicker.remove();
        }
    });
}