from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

#
# helper function to help generate permalinks of entries
#
def permalink(value):
	if value.__class__.__name__ == 'Entry':
		return value.permalink()
	else:
		raise Exception( 'The permalink filter only works on instances of the Entry class')

#
# this is all necessary so that our custom filter is registered within django's filters
#
register = webapp.template.create_template_register()
register.filter(permalink)
webapp.template.register_template_library('app.utils.templatehelpers')