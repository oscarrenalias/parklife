import unittest
from app.tests.testkit import *

#
# unit tests for the RESTful services provided by Parklife
# (both authenticated and non-authenticated services)
#

class RestTestCase(unittest.TestCase):
	# base URL of our site / TODO: can we retrieve this from Defaults?
	baseUrl = "http://localhost:8081"

	# call getLoginCookie to initialize this value (dev_appserver_login)
	cookie = {}

	def uri(self, uriPart):
		return self.baseUrl + uriPart

	# needed for the services that require authentication, will generate a cookie
	# that we must provide with every further authenticated request
	def login(self, auth={ 'user': "test@example.com", 'password': 'password'}):
		# we need to prevent httplib2 from following the redirect, otherwise we lose the auth cookie
		resp, data = HttpTestKit.doHttp(self.uri("/_ah/login?email=" + auth['user'] + "&admin=True&action=Login"), redirects=False)

		# retrieve the cookie with a regexp and save it
		import re
		self.cookie = {'dev_appserver_login': re.findall("dev_appserver_login=\"(.*)\"; Path=/", resp['set-cookie'])[0]}	

#
# Tests for the JSon services
#
class TestJSonBlogServices(RestTestCase):
	def assertResponse(self, resp):
		self.assertEquals('200', resp['status'])
		self.assertEquals("application/json; charset=utf-8", resp['content-type'])

	def testFrontPageJSon(self):
		resp, data = HttpTestKit.doRest(self.uri("/?f=json"))
		self.assertResponse(resp)
	
	def testTagsJSon(self):
		resp, data = HttpTestKit.doRest(self.uri("/tag/test?f=json"))
		self.assertResponse(resp)

	def testSourcesJSon(self):
		resp, data = HttpTestKit.doRest(self.uri("/source/twitter?f=json"))
		self.assertResponse(resp)

#
# Tests for the Atom services
#
class TestAtomBlogServices(RestTestCase):
	def assertResponse(self, resp):
		self.assertEquals('200', resp['status'])
		self.assertEquals("application/atom+xml; charset=utf-8", resp['content-type'])


	def testFrontPageAtom(self):
		resp, data = HttpTestKit.doRest(self.uri("/?f=atom"), decoder=XmlDecoder())
		self.assertResponse(resp)
	
	def testTagsAtom(self):
		resp, data = HttpTestKit.doRest(self.uri("/tag/test?f=atom"), decoder=XmlDecoder())
		self.assertResponse(resp)

	def testSourcesAtom(self):
		resp, data = HttpTestKit.doRest(self.uri("/source/twitter?f=atom"), decoder=XmlDecoder())
		self.assertResponse(resp)		

#
# Tests for the JSON Ajax interfaces 	
#
class TestAdminServices(RestTestCase):
	def assertResponse(self, resp):
		self.assertEquals('200', resp['status'])
		self.assertEquals("application/json; charset=utf-8", resp['content-type'])
		
	# tests that the security filter works
	def testCreateEntryNoAuth(self): 
		resp, data = HttpTestKit.doRest(self.uri("/service/entry/"), method="POST")
		self.assertEquals("302", resp["status"])

	# tests that entries can be created
	def testCreateEntry(self): 
		# body for the request
		import datetime
		body = "id_title=title_" + str(datetime.datetime.now().microsecond) + "&id_text=text&id_tags=tags&lat=&lng="
		# log in and set the cookie
		self.login()
		# make the call, with the auth cookie
		resp, data = HttpTestKit.doRest(self.uri("/service/entry/"), method="POST", body=body, cookies=self.cookie)

		# check the outcome
		self.assertResponse(resp)

		# get the permalink
		link = data['entry']['service_link']
		# and retrieve it to make sure that everything worked fine
		resp2, data2 = HttpTestKit.doRest(link, cookies=self.cookie)
		self.assertResponse(resp2)

		# compare the two entries
		self.assertEquals(data['entry']['text'], data2['entry']['text'])
		self.assertEquals(data['entry']['title'], data2['entry']['title'])
		self.assertEquals(data['entry']['tags'], data2['entry']['tags'])

	# failure when creating an entry
	def testFailedCreateEntry(self): 
		# body for the request
		import datetime
		body = "id_title=&id_text=&id_tags=tags&lat=&lng="
		# log in and set the cookie
		self.login()
		# make the call, with the auth cookie
		resp, data = HttpTestKit.doRest(self.uri("/service/entry/"), method="POST", body=body, cookies=self.cookie)

		# check the outcome
		self.assertResponse(resp)

		# there should be an error
		self.assertTrue(data['error'])
		# and two error messages
		self.assertEquals(2, len(data['errors']))

	# tests that entries can be deleted
	def testDeleteEntry(self):
		# body for the request
		import datetime
		body = "id_title=title_" + str(datetime.datetime.now().microsecond) + "&id_text=text&id_tags=tags&lat=&lng="
		# log in and set the cookie
		self.login()
		# make the call, with the auth cookie
		resp, data = HttpTestKit.doRest(self.uri("/service/entry/"), method="POST", body=body, cookies=self.cookie)

		# check the outcome
		self.assertResponse(resp)

		# now delete the entry
		link = data['entry']['service_link']
		# and retrieve it to make sure that everything worked fine
		resp2, data2 = HttpTestKit.doRest(link, method="DELETE", cookies=self.cookie)
		self.assertResponse(resp2)
		# make sure it was deleted
		self.assertFalse(data2['error'])

		# make sure that it doesn't exist anymore	
		resp3, data3 = HttpTestKit.doRest(link, cookies=self.cookie)
		self.assertResponse(resp3)
		# the entry actually exists, but the deletion flag will be set to true
		self.assertTrue(data3['entry']['deleted'])