// // Copyright (c) 2025, A and contributors
// // For license information, please see license.txt

// // frappe.ui.form.on("Airplane Ticket", {
// // 	refresh(frm) {

// // 	},
// // });
// // frappe.ui.form.on('Airplane Ticket', {
// //     refresh: function(frm) {
// //         // Add a custom button
// //         frm.add_custom_button('Assign Seat', function() {
// //             // Create a dialog to enter seat number
// //             let d = new frappe.ui.Dialog({
// //                 title: 'Enter Seat Number',
// //                 fields: [
// //                     {
// //                         label: 'Seat Number',
// //                         fieldname: 'seat_number',
// //                         fieldtype: 'Data',
// //                         reqd: 1
// //                     }
// //                 ],
// //                 primary_action_label: 'Set Seat',
// //                 primary_action(values) {
// //                     frm.set_value('seat', values.seat_number);  // Set seat number in the form
// //                     d.hide();
// //                 }
// //             });

// //             d.show();
// //         });
// //     }
// // });

frappe.ui.form.on('Airplane Ticket', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {  // Only show button for saved records
            frm.add_custom_button(__('Assign Seat'), function() {
                frappe.prompt([
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1
                    }
                ], (values) => {
                    frm.set_value('seat', values.seat_number);
                    frm.save();
                }, __('Assign Seat'), __('Assign'));
            });
        }
    }
});



// Copyright (c) 2025, Sanskar and contributors
// For license information, please see license.txt

~


