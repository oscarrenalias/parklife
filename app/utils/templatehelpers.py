#
# helper function to help generate permalinks of entries
#
from jinja2.filters import environmentfilter

class templatehelpers:
	
	@staticmethod
	def permalink(value):
		if value.__class__.__name__ == 'Entry':
			return value.permalink()
		else:
			raise Exception( 'The permalink filter only works on instances of the Entry class')
			
	#
	# helper function to format a date to the RFC 3339 date used in Atom feeds
	#
	@staticmethod	
	def atom_date(value):
		if value.__class__.__name__ != "datetime":
			raise Exception( 'This filter can only be used with datetime objects' )
			
		return(value.strftime("%Y-%m-%dT%H:%M:%SZ"))

	#
	# slugifies values
	#
	@staticmethod	
	def slugify(value):
		import re
		aslug = re.sub('[^\w\s-]', '', value).strip().lower()
		aslug = re.sub('\s+', '-', aslug)
		return aslug

	#
	# formats dates with the given format
	#
	@staticmethod
	def date_format(value, format="%B %d, %Y"):
		if value.__class__.__name__ == "str":
			# convert the date to a date object
			from app.dateutil.parser import parse
			value = parse(value)

		return value.strftime(format)

	#
	# Improved method of Jinja's groupby filter where we can provide an attribute name
	# that is actually an instance method, and not just an attribute
	#
	@staticmethod
	def do_groupby_new(value, attribute, reverse=False):
		from jinja2.filters import _GroupTuple
		from itertools import groupby
		expr = lambda x: do_call(x, attribute)
		return sorted(map(_GroupTuple, groupby(sorted(value, key=expr), expr)), reverse=reverse)	

#
# Calls a method or retrieves the attribute of an instance by its name, provided
# as a string
# TODO: where to put this?
#
def do_call(obj, attribute):
	v = getattr(obj, attribute)
	if v.__class__.__name__ == "instancemethod":
		return v()
	else:
		return v