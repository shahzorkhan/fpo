// Copyright (c) 2016, Shahzor Khan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farmer Quotation', {
	refresh: function(frm) {
        var doc = frm.doc;
        if(doc.docstatus==1) {
			if(doc.status == 'Submitted' && doc.quotation_type == 'Procurement') {
				// delivery note
				frm.add_custom_button(__('Purchase Invoice'),
					function() {
					    frappe.model.open_mapped_doc({
                                method: "fpo.fpo.doctype.farmer_quotation.farmer_quotation.make_purchase_invoice",
                                frm: me.frm
                            })
					     }, __("Make"));
            }
        }
	}
});
