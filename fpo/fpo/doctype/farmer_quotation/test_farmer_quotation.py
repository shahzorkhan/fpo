# -*- coding: utf-8 -*-
# Copyright (c) 2015, Shahzor Khan and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

# test_records = frappe.get_test_records('Farmer Quotation')

class TestFarmerQuotation(unittest.TestCase):
	def test_make_farmer_quotation(self):
		fq = create_farmer_quotation(do_not_submit=True)

def create_farmer_quotation(**args):
	fq = frappe.new_doc("Farmer Quotation")
	args = frappe._dict(args)
	if args.transaction_date:
		fq.transaction_date = args.transaction_date

	fq.company = args.company or "_Test Company"
	fq.farmer = args.farmer or "_Test Farmer"
	fq.quotation_type = args.is_subcontracted or "Procurement"
	fq.currency = args.currency or frappe.db.get_value("Company", fq.company, "default_currency")
	fq.conversion_factor = args.conversion_factor or 1

	fq.append("items", {
		"item_code": args.item or args.item_code or "_Test Item",
		"description": args.item or args.description or args.item_code or "_Test Item",
		"qty": args.qty or 10,
		"rate": args.rate or 500,
		"grade": args.grade or "A",
		"uom": args.uom or "Box"
	})
	if not args.do_not_save:
		fq.insert()
		if not args.do_not_submit:
			fq.submit()

	return fq

