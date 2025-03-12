// Copyright (c) 2025, A and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airline', {
    refresh: function(frm) {
        if (frm.doc.website) {
            // Remove existing link to prevent duplicates
            $('.custom-website-link').remove();

            // Create the link element
            let website_link = $(`
                <a class="custom-website-link"
                    href="${frm.doc.website}"
                    target="_blank"
                    style="display:block; margin-bottom:10px; font-weight:bold;">
                    Visit Website
                </a>
            `);

            // Append it inside the sidebar
            frm.page.sidebar.find('.form-assignments').prepend(website_link);
        }
    }
});

