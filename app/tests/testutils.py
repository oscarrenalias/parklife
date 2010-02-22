import unittest
from app.utils import Utils

class TestUtils(unittest.TestCase):
	
	def testlinks_to_anchors(self):
		data = [
			{ 'input': 'this is a http://test.com test', 'expected': 'this is a <a href="http://test.com">http://test.com</a> test' },
			{ 'input': 'this is a http://test.com#asdf test', 'expected': 'this is a <a href="http://test.com#asdf">http://test.com#asdf</a> test' },
			{ 'input': 'this is a http://test.com?asdf=lala test', 'expected': 'this is a <a href="http://test.com?asdf=lala">http://test.com?asdf=lala</a> test' },
			{ 'input': 'nothing', 'expected': 'nothing' },
			{ 'input': '', 'expected': ''}
		]

		for test in data:
			self.assertEqual( test['expected'], Utils.links_to_anchors( test['input'] ))
		
	def testtwitpic_to_img(self):
		data = [
			{ 'input': 'this is an image http://twitpic.com/213akl', 'expected': 'this is an image <div class="twitpic_img"><a href="http://twitpic.com/213akl"><img src="http://twitpic.com/show/large/213akl" width="350" alt="213akl"/></a></div>' }
		]

		for test in data:
			self.assertEqual( test['expected'], Utils.twitpic_to_img( test['input'] ))