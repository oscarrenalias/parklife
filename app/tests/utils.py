import unittest
from app.utils import Utils

class TestUtils(unittest.TestCase):
	
	def testlinks_to_anchors(self):
		data = [
			{ 'input': 'this is a http://test.com test', 'expected': 'this is a <a href="http://test.com">http://test.com</a> test' },
			{ 'input': 'this is a http://test.com#asdf test', 'expected': 'this is a <a href="http://test.com#asdf">http://test.com#asdf</a> test' },
			{ 'input': 'this is a http://test.com?asdf=lala test', 'expected': 'this is a <a href="http://test.com?asdf=lala">http://test.com?asdf=lala</a> test' },
			{ 'input': 'nothing', 'expected': 'nothing' },
			{ 'input': '', 'expected': ''},
			{ 'input': 'asdfasdf http://twitpic.com/adsfk32', 'expected': 'asdfasdf http://twitpic.com/adsfk32' }
		]

		self._runTests( data, Utils.links_to_anchors )
		
	def testtwitpic_to_img(self):
		data = [
			{ 'input': 'this is an image http://twitpic.com/213akl', 'expected': 'this is an image <div class="twitpic_img"><a href="http://twitpic.com/213akl"><img src="http://twitpic.com/show/large/213akl" width="350" alt="213akl"/></a></div>' }
		]
		self._runTests(data, Utils.twitpic_to_img )
			
	def testsequence(self):
		data = [
			{ 'input': 'http://test.com asdfasdf http://twitpic.com/adsfk32', 'expected': '<a href="http://test.com">http://test.com</a> asdfasdf <div class="twitpic_img"><a href="http://twitpic.com/adsfk32"><img src="http://twitpic.com/show/large/adsfk32" width="350" alt="adsfk32"/></a></div>' }
		]
		# just testing that we get the same result regardless of the order
		f1 = lambda str: Utils.twitpic_to_img(Utils.links_to_anchors(str))
		f2 = lambda str: Utils.links_to_anchors(Utils.twitpic_to_img(str))		
		self._runTests( data, f1 )
		self._runTests( data, f2 )
		
	#
	# tests the StringHelper extract_twitter_tags
	#
	def test_StringHelper_extract_twitter_tags(self):
		data = [
			{'input': 'this is a test', 'expected': [] },
			{'input': 'this is a #test', 'expected': ['test'] },
			{'input': 'test: #these #are #many #tags, or not?', 'expected': ['these', 'are', 'many', 'tags' ]}			
		]
		from app.utils import StringHelper		
		str_helper = StringHelper()
		
		for test in data:
			self.assertEqual( test['expected'], str_helper.extract_twitter_tags(test['input']))
		
	def _runTests(self, test_data, func ):
		for test in test_data:
			self.assertEqual( test['expected'], func( test['input'] ))