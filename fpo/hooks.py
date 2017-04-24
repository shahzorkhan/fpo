# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "fpo"
app_title = "FPO"
app_publisher = "Shahzor Khan"
app_description = "ERP solution for Farmer Producer Organizations"
app_icon = "octicon octicon-globe"
app_color = "green"
app_email = "shahzorkhan123@yahoo.co.in"
app_license = "MIT"

# Includes in <head>
# ------------------


app_include_js = [
    "assets/js/fpo.min.js"
]
app_include_css = [
    "assets/css/fpo.css"
]
web_include_js = [
    "assets/js/fpo-web.min.js"
]
#web_include_css = [
#    "assets/css/fpo.css"
#]

# include js, css files in header of desk.html
# app_include_css = "/assets/fpo/css/fpo.css"
# app_include_js = "/assets/fpo/js/fpo.js"

# include js, css files in header of web template
# web_include_css = "/assets/fpo/css/fpo.css"
# web_include_js = "/assets/fpo/js/fpo.js"
# web_include_js = "/assets/fpo/js/fpo.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "fpo.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "fpo.install.before_install"
# after_install = "fpo.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "fpo.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"fpo.tasks.all"
# 	],
# 	"daily": [
# 		"fpo.tasks.daily"
# 	],
# 	"hourly": [
# 		"fpo.tasks.hourly"
# 	],
# 	"weekly": [
# 		"fpo.tasks.weekly"
# 	]
# 	"monthly": [
# 		"fpo.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "fpo.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "fpo.event.get_events"
# }

