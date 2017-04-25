# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "FPO",
			"color": "green",
			"icon": "octicon octicon-globe",
			"type": "module",
			"label": _("FPO")
		},
		{
			"module_name": "POP",
			"color": "#589494",
			"icon": "fa fa-th",
			"icon": "octicon octicon-credit-card",
			"type": "page",
			"link": "pop",
			"label": _("POP")
		}
	]
