# -*- coding: utf-8 -*-
# Copyright (c) 2015, Shahzor Khan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt
from frappe.utils import add_days, getdate, formatdate, get_first_day, date_diff, add_years, get_timestamp

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
        if self.status != "Promoted":
            self.status = fq_status_map[self.docstatus or 0]

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        set_supplier(source, target)
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")
        source.purchase_invoice = target.name
        source.status = "Promoted"
        frappe.throw(("Due Date {0} cannot be before Posting Date {1}").format(target.due_date, target.posting_date))

        target.save()
        source.save()
        frappe.db.commit()

    def set_supplier(source, target):
        farmer = frappe.get_doc("Farmer", source.get('farmer'))

        if not frappe.db.exists('Supplier Type', 'Farmer'):
            supplier_type = frappe.new_doc('Supplier_Type')
            supplier_type.supplier_type = 'Farmer'
            supplier_type.save(ignore_permissions=True)
            frappe.db.commit()

        supplier = frappe.db.get_value('Supplier', {"supplier_name": farmer.get('title')}, ["name", 'supplier_name'], as_dict=1)

        if supplier is None:
            supplier_doc = frappe.new_doc('Supplier')
            supplier_doc.name = farmer.get('name')
            supplier_doc.supplier_name = farmer.get('title')
            supplier_doc.image = farmer.get('image')
            supplier_doc.supplier_type = 'Farmer'
            supplier_doc.supplier_details = farmer.get("address")+ "\r\n"+ farmer.get('bank_details')
            supplier_doc.save()
            frappe.db.commit()

            supplier = frappe.db.get_value('Supplier', {"supplier_name": farmer.get('title')}, ["name", 'supplier_name'], as_dict=1)

        if not frappe.db.exists('Supplier', supplier.get('name')):
            frappe.throw((
                'Could not create supplier from farmer frappe.db.exists("Supplier", ID) failed for {0}')
                         .format(supplier.get('name')))

        credit_days_based_on, credit_days, supplier_type = \
            frappe.db.get_value('Supplier', supplier.get('name'), ["credit_days_based_on", "credit_days", "supplier_type"])

        target.supplier = supplier.get('name')

    doclist = get_mapped_doc("Farmer Quotation", source_name,     {
        "Farmer Quotation": {
            "doctype": "Purchase Invoice",
            "validation": {
                "docstatus": ["=", 1],
                "status": ["=", "Submitted"],
                "quotation_type": ["=", "Procurement"]
            },
            "field_map": {
                "transaction_date": "posting_date",
                "grand_total": "grand_total",
                "in_words": "in_words",
                "currency": "currency",
                "conversion_rate": "conversion_rate",
                "name": "title"
            }
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
            }
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
