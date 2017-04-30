from frappe import _

def get_data():
	return {
		'fieldname': 'farmer_quotation',
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Purchase Invoice']
			}
		]
	}