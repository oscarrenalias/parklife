from app.httplib2 import *

#
# These classes are responsible for decoding responses from the service
#
class BaseDecoder:
	@staticmethod
	def decode(content):
		return content

#
# Decoder of JSON responses
#
class JSonDecoder(BaseDecoder):
	@staticmethod
	def decode(content):
		import simplejson as json
		return json.loads(content)

#
# Decoder for XML responses (such as Atom). Uses the ElementTree parser
#
class XmlDecoder(BaseDecoder):
	@staticmethod
	def decode(content):
		from xml.etree import ElementTree
		return ElementTree.fromstring(content)


class HttpTestKit:

	@staticmethod
	def doHttp(url, method="GET", body=None, headers=None, basicAuth={}, redirects=False, cookies=None):
		http = Http()

		http.follow_redirects = redirects

		# add security credentials for basic authentication
		if len(basicAuth) == 2:
			http.add_credentials(basicAuth['user'], basicAuth['password'])

		# are there cookies?
		if cookies:
			# initialize the headers if none was provided
			if headers == None:
				headers = {}

			for (name,value) in cookies.iteritems():
				headers['Cookie'] = name + '="' + value + '"'

		response = http.request(url, method=method, body=body, headers=headers)
		return response[0], response[1] 

	#
	# Performs a REST call and returns the content decoded in the given decoder.
	# Ddefaults to JSonDecoder and GET as the method
	#
	@staticmethod
	def doRest(url, decoder=JSonDecoder(), method="GET", body=None, headers=None, cookies=None, basicAuth={}):
		response, data = HttpTestKit.doHttp(url, method=method, body=body, headers=headers, cookies=cookies, basicAuth=basicAuth)

		if response['status'] == '200':
			return response, decoder.decode(data)
		else:
			# there was an error, so there is no data
			return response, None