# -*- coding: utf-8 -*-
# Copyright (c) 2015, Shahzor Khan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Farmer(Document):
	def autoname(self):
		self.name = self.title
		#self.name = make_autoname(self.naming_series + '.#####')
