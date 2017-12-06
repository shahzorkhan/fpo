# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.utils import nowdate
from erpnext.setup.utils import get_exchange_rate
from erpnext.stock.get_item_details import get_pos_profile
from erpnext.accounts.party import get_party_account_currency
from erpnext.controllers.accounts_controller import get_taxes_and_charges

@frappe.whitelist()
def get_pop_data():
	doc = frappe.new_doc('Farmer Quotation')
	doc.is_pop = 1;
	pos_profile = get_pos_profile(doc.company) or {}
	if not doc.company: doc.company = pos_profile.get('company')
	doc.update_stock = 0;#pos_profile.get('update_stock')

	if pos_profile.get('name'):
		pos_profile = frappe.get_doc('POS Profile', pos_profile.get('name'))

	company_data = get_company_data(doc.company)
	update_pos_profile_data(doc, pos_profile, company_data)
	default_print_format = "Point of Purchase" #pos_profile.get('print_format') or
		
	print_template = frappe.db.get_value('Print Format', default_print_format, 'html')

	return {
		'doc': doc,
		'items': get_items_list(),
		'item_uoms': get_items_uoms(),
		'farmers': get_farmers_list(),
		'print_template': print_template,
		'meta': get_meta()
	}

def get_meta():
	doctype_meta = {
		'farmer': frappe.get_meta('Farmer'),
		'quotation': frappe.get_meta('Farmer Quotation')
	}

	for row in frappe.get_all('DocField', fields = ['fieldname', 'options'],
		filters = {'parent': 'Farmer Quotation', 'fieldtype': 'Table'}):
		doctype_meta[row.fieldname] = frappe.get_meta(row.options)

	return doctype_meta

def get_company_data(company):
	return frappe.get_all('Company', fields = ["*"], filters= {'name': company})[0]

def update_pos_profile_data(doc, pos_profile, company_data):
	doc.campaign = pos_profile.get('campaign')
	print()
	doc.write_off_account = pos_profile.get('write_off_account') or \
		company_data.write_off_account
	doc.change_amount_account = pos_profile.get('change_amount_account') or \
		company_data.default_cash_account
	doc.taxes_and_charges = pos_profile.get('taxes_and_charges')

	doc.currency = pos_profile.get('currency') or company_data.default_currency
	doc.conversion_rate = 1.0
	doc.company_address = company_data.address
	doc.company_email = company_data.email
	doc.company_phone_no = company_data.phone_no
	doc.company_website = company_data.website

	if doc.currency != company_data.default_currency:
		doc.conversion_rate = get_exchange_rate(doc.currency, company_data.default_currency, doc.posting_date)
	doc.territory = pos_profile.get('territory') or get_root('Territory')

def get_root(table):
	root = frappe.db.sql(""" select name from `tab%(table)s` having
		min(lft)"""%{'table': table}, as_dict=1)

	return root[0].name

def get_items_list():
	cond = "1=1"
	item_groups = []
	return frappe.db.sql(""" 
		select
			name, item_code, item_name, description, item_group, expense_account, has_batch_no,
			has_serial_no, expense_account, selling_cost_center, stock_uom, image, 
			default_warehouse, is_stock_item, barcode
		from
			tabItem
		where
			disabled = 0 and has_variants = 0 and is_purchase_item = 1 and {cond}
		""".format(cond=cond), tuple(item_groups), as_dict=1)

def get_items_uoms():

	return frappe.db.sql("""
		select
			name, conversion_factor, uom , parent
		from
			`tabUOM Conversion Detail`
		 where
		 	parenttype = 'Item' and parentfield = 'uoms'
		order by parent,idx
		""", as_dict=1)

def get_farmers_list():

	return frappe.db.sql(""" select name, title, id, village, cluster, kcc, shg, farmer_group, address, bank_account, bank_ifsc, bank_name, mobile from tabFarmer where disabled = 0""",
		as_dict=1) or {}

@frappe.whitelist()
def make_farmer_quotation(doc_list):
	if isinstance(doc_list, basestring):
		doc_list = json.loads(doc_list)

	name_list = []

	for docs in doc_list:
		for name, doc in docs.items():
			if not frappe.db.exists('Farmer Quotation', {'offline_pop_name': name}):
				validate_records(doc)
				fq_doc = frappe.new_doc('Farmer Quotation')
				fq_doc.offline_pop_name = name
				fq_doc.update(doc)
				submit_farmer_quotation(fq_doc, name)
				name_list.append(name)
			else:
				name_list.append(name)

	return name_list

def validate_records(doc):
	validate_farmer(doc)
	validate_item(doc)

def validate_farmer(doc):
	if not frappe.db.exists('Farmer', doc.get('farmer')):
		farmer_doc = frappe.new_doc('Farmer')
		farmer_doc.customer_name = doc.get('farmer')
		farmer_doc.save(ignore_permissions = True)
		frappe.db.commit()
		doc['farmer'] = farmer_doc.name

def validate_item(doc):
	for item in doc.get('items'):
		if not frappe.db.exists('Item', item.get('item_code')):
			item_doc = frappe.new_doc('Item')
			item_doc.name = item.get('item_code')
			item_doc.item_code = item.get('item_code')
			item_doc.item_name = item.get('item_name')
			item_doc.description = item.get('description')
			item_doc.default_warehouse = item.get('warehouse')
			item_doc.stock_uom = item.get('stock_uom')
			item_doc.item_group = item.get('item_group')
			item_doc.save(ignore_permissions=True)
			frappe.db.commit()

def submit_farmer_quotation(fq_doc, name):
	try:
		fq_doc.insert()
		fq_doc.submit()
		frappe.db.commit()
	except Exception, e:
		if frappe.message_log: frappe.message_log.pop()
		frappe.db.rollback()
		save_farmer_quotation(e, fq_doc, name)

def save_farmer_quotation(e, fq_doc, name):
	if not frappe.db.exists('Farmer Quotation', {'offline_pop_name': name}):
		fq_doc.docstatus = 0
		fq_doc.flags.ignore_mandatory = True
		fq_doc.insert()
