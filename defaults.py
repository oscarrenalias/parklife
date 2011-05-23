#
# class with some global settings
#

class Defaults:
	
	# amount of posts per page
	POSTS_PER_PAGE = 15
	
	# YouTube API key
	YOUTUBE_API_KEY = 'AI39si4eYUVgiR7wTB5h4BL9XvQWO1VkQn9B9x_bZKZMC00y8SMfS66aky8qzmOYyifLiF-e-dFhW3n1VrgBAp62O_4GOKyObw'
	
	# Google Search Ajax API key
	GOOGLE_API_KEY = 'ABQIAAAAlefqhB0S3KPTMC9Eyh9uPRRyzxWefuPwDWzRUAiaxlmoyqrEThQ5HlU0jq4VYv1d914ChLVitmcZYQ'
	
	# Google Maps API key
	GOOGLE_MAPS_API_KEY = 'ABQIAAAAlefqhB0S3KPTMC9Eyh9uPRQ07NP0L6lw46OYIIZDiaOMe_2IihQskZS8kMpydvEAAgkw1rcZMzCoBQ'
	
	# Custom searh engine key
	GOOGLE_CUSTOM_SEARCH_ENGINE_KEY = '011990932543207137146:wcze-5xmxso'
	
	# ignore twitter @ replies?
	TWITTER_IGNORE_AT_REPLIES = True
	
	# what image size to use from Instagram?
	# As per the current API, it must be one of these:
	#	'low_resolution'
	#	'standard_resolution'
	# 	'thumbnail'
	INSTAGRAM_IMAGE_SIZE = 'low_resolution'
	
	# for the pinboard source, ignore those links whose title is "Instagram", so that
	# we don't get multiple entries for the same Instagram picture if both the Instagram
	# and the Pinboard sources are enabled
	PINBOARD_IGNORE_INSTAGRAM_LINKS = True
	
	# enable or disable comments, as well as the disqus key
	COMMENTS_ENABLED = True
	DISQUS_USER = 'renaliasnet'
	
	# default time to live for the memcache cached keys, in seconds
	MEMCACHE_TTL = 3600
	
	@staticmethod
	def isDevelopmentServer():
		import os
		return(os.environ['SERVER_SOFTWARE'].startswith('Dev'))
		
	# site data
	site = {
	  'base_url': 'http://stream.renalias.net',
	  'author': 'Oscar Renalias',
	  'email': 'oscar+lifestream@renalias.net',
	  'title': 'Oscar Renalias',
	  'subtitle': 'Oscar Renalias'
	}
	
# makes things easier in the development setup
if Defaults.isDevelopmentServer():
	Defaults.site['base_url'] = 'http://localhost:8081'