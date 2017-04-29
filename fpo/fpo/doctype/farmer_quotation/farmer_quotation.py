# -*- coding: utf-8 -*-
# Copyright (c) 2015, Shahzor Khan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt

fq_status_map = {
    0: "Draft",
    1: "Submitted",
    2: "Cancelled"
}

class FarmerQuotation(Document):
    def validate(self):
        self.set_status_from_docStatus()
        pass

    def set_status_from_docStatus(self):
        #        if not self.status and not not self.docstatus:
        # if not not self.docstatus  :
        print (self.docstatus)
        print (self.status)
        self.status = fq_status_map[self.docstatus or 0]

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")
        set_supplier(source, target)

    def set_supplier(source, target):
        farmer = frappe.get_doc("Farmer", source.get('farmer'))

        if not frappe.db.exists('Supplier Type', 'Farmer'):
            supplier_type = frappe.new_doc('Supplier_Type')
            supplier_type.supplier_type = 'Farmer'
            supplier_type.save(ignore_permissions=True)
            frappe.db.commit()

        if not frappe.db.exists('Supplier', source.get('farmer')):
            supplier_doc = frappe.new_doc('Supplier')
            supplier_doc.name = farmer.get('name')
            supplier_doc.image = farmer.get('image')
            supplier_doc.supplier_type = 'Farmer'
            supplier_doc.supplier_details = farmer.get("address")+ "\r\n"+ farmer.get('bank_details')
            frappe.db.commit()

        target.supplier = farmer.get('name')

    def update_quotation(source_doc, target_doc, source_parent):
        target_doc.from_farmer_quotation = source_doc.name
        source_doc.status = "Promoted"

    def update_item(source_doc, target_doc, source_parent):
        #target_doc.base_amount = flt(source_doc.qty) * flt(source_doc.base_rate)
        target_doc.amount = flt(source_doc.qty)  * flt(source_doc.rate)
        target_doc.qty = flt(source_doc.qty)

    doclist = get_mapped_doc("Farmer Quotation", source_name,     {
        "Farmer Quotation": {
            "doctype": "Purchase Invoice",
            "validation": {
                "docstatus": ["=", 1],
                "quotation_type": ["=", "Procurement"]
            },
            "field_map": {
                "transaction_date": "posting_date",
                "grand_total": "grand_total",
                "in_words": "in_words",
                "currency": "currency",
                "conversion_rate": "conversion_rate",
                "name": "title"
            },
            "postprocess": update_quotation,
        },
        "Farmer Quotation Item": {
            "doctype": "Purchase Invoice Item",
            "field_map": {
                "item_code": "item_code",
                "item_name": "item_name",
                "grade": "grade",
                "qty": "qty",
                "uom": "uom",
                "rate": "rate",
                "amount": "amount",
            },
            "postprocess": update_item
        }
        # ,
        # "Sales Taxes and Charges": {
        #     "doctype": "Sales Taxes and Charges",
        #     "add_if_empty": True
        # },
        # "Sales Team": {
        #     "doctype": "Sales Team",
        #     "field_map": {
        #         "incentives": "incentives"
        #     },
        #     "add_if_empty": True
        # }
    }, target_doc, set_missing_values)

    return doclist
