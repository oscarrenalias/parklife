#
# module containing some utility functions
#

import re

class Utils:
	#
	# turns plain HTTP links into anchors. A bit crude but it works
	#
	@staticmethod
	def links_to_anchors( text, ignore_twitpic_links = True ):
	
		urlmatch = re.compile(r'https?://\S+')  
		urls = urlmatch.findall( text )
		for u in urls:
			if u.find('http://twitpic.com') == -1:
				text = text.replace(u,'<a href="' + u + '">' + u + '</a>')
	
		return text
	
	#
	# turns twitpic links into img tags
	#
	@staticmethod	
	def twitpic_to_img( text ):
		urlmatch = re.compile(r'https?://twitpic.com/(\S+)')
		urls = urlmatch.findall( text )
		for u in urls:
			twitpic_link = 'http://twitpic.com/' + u
			img_link = 'http://twitpic.com/show/large/' + u
			text = text.replace(u,'<div class="twitpic_img"><a href="' + twitpic_link + '"><img src="' + img_link + '" width="350" alt="' + u + '"/></a></div>')
			# crude, but it works
			text = text.replace('http://twitpic.com/<div', '<div')
	
		return text