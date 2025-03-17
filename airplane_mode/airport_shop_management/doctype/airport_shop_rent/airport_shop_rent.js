// Copyright (c) 2025, A and contributors
// For license information, please see license.txt


frappe.ui.form.on('Airport Shop Rent', {
    refresh: function(frm) {
        frm.set_query("shop", function() {
            return {
                filters: {
                    "status": "On Lease"
                }
            };
        });
    },
    status: function(frm) {
        if (frm.doc.status === "Pending") {
            frm.set_value("paid_amount", "");
        } else {
            if (frm.doc.shop) {
                frappe.db.get_value("Shop", frm.doc.shop, "rent_amount", (r) => {
                    if (r && r.rent_amount) {
                        frm.set_value("paid_amount", r.rent_amount);
                    }
                });
            }
        }
    }
});
