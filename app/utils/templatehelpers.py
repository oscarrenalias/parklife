#
# helper function to help generate permalinks of entries
#
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