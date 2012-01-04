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
	def is_mobile(ua):
		return ViewHelpers._is_useragent(ua, _IPHONE_UA)

	@staticmethod
	def select_output(request):
		if request == None:
			output = 'html'
		else:
			if request.get('f') != '':	# we're being forced to return some content
				output = request.get('f')
			else:
				if ViewHelpers.is_mobile(request.headers['user-agent']):	# mobile takes the next priority
					output = 'mobile'
				else:
					output = 'html'	# otherwise return plain html

		return output