import webapp2
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
# helper function to format a date to the RFC 3339 date used in Atom feeds
#
def atom_date(value):
	if value.__class__.__name__ != "datetime":
		raise Exception( 'This filter can only be used with datetime objects' )
		
	return(value.strftime("%Y-%m-%dT%H:%M:%SZ"))

#
# this is all necessary so that our custom filter is registered within django's filters
#
#register = webapp2.template.create_template_register()
#register.filter(permalink)
#register.filter(atom_date)
#webapp2.template.register_template_library('app.utils.templatehelpers')