from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("FPO"),
			"items": [
				{
					"type": "doctype",
					"name": "Farmer",
					"description": _("List of Farmers.")
				},
				{
					"type": "doctype",
					"name": "Farmer Quotation",
					"description": _("Quotation raised by Farmers.")
				},
				{
					"type": "page",
					"name": "pop",
					"label": _("POP"),
					"description": _("Point of Purchase")
				}
			]

		}
	]
