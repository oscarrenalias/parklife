import unittest
from app.view.viewhelpers import ViewHelpers

class TestViewHelpers(unittest.TestCase):
	
	def testiPhoneUARegex(self):
		# should match
		self.assertEqual(True, 
			ViewHelpers.is_iphone('Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'))
			
		# should not match
		self.assertEqual(False, 
			ViewHelpers.is_iphone('whatever'))			
			
	def testiPadUA(self):
		# should not match either, this is the iPad user agent string
		self.assertEqual(False, 
			ViewHelpers.is_iphone('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'))		
				