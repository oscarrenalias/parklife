import re

#
# regular expression, iPhone only (not ipad)
#		
_IPHONE_UA = re.compile(r'iPhone.*Mobile.*Safari')

class ViewHelpers:
	@staticmethod
	def _is_useragent(ua, pattern):
		return pattern.search(ua) is not None
		
	@staticmethod
	def is_iphone(ua):
		return ViewHelpers._is_useragent(ua, _IPHONE_UA)