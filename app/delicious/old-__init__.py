from base64 import b64encode
from urllib import urlencode
import urllib2

def _py26OrGreater():
    import sys
    return sys.hexversion > 0x20600f0

if _py26OrGreater():
    import json
else:
    import app.simplejson as json

class Delicious:
	
	def __init__(self, user = '', password = ''):
		self.user = user
		self.password = password
		
		self.domain = 'feeds.delicious.com'
		self.base_uri = '/v2/json'
		
	def user_feed(self, count = 100):
		uri = self.base_uri + '/' + self.user
		return self.__delicious_call( uri, { 'count': count })
		
	def __delicious_call(self, uri, params):
		req = urllib2.Request("http://%s/%s?count=%s" %(self.domain, uri, params['count'] ))
		try:
			handle = urllib2.urlopen(req)
			return json.loads(handle.read())
		except urllib2.HTTPError, e:
			if (e.code == 304):
				return []
			else:
				raise Exception( 'Error making Delicious API call' )
				
if __name__ == '__main__':
	d = Delicious('phunkphorce')
	print d.user_feed(1)