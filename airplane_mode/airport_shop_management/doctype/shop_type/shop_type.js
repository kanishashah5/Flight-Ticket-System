// Copyright (c) 2025, A and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
    refresh: function(frm) {
        frm.set_query("shop_type", function() {
            return {
                filters: {
                    enabled: 1
                }
            };
        });
    }
});
