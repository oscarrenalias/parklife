from google.appengine.api import memcache
import logging
from app.pager.pager import PagerQuery
from defaults import Defaults

class CachedQuery(PagerQuery):
	
	#
	# Extends PagedQuery::fetch() by providing caching
	# mechanisms via memcache
	#
	def fetch(self, limit, bookmark=None):
		cache_key = self._generate_key_for_query(limit, bookmark)
		data = memcache.get(cache_key)
		if data == None:
			logging.info('Cache miss: key = ' + cache_key)
			data = super(CachedQuery, self).fetch(limit, bookmark)
			memcache.add(cache_key, value=data, time=Defaults.MEMCACHE_TTL)
		else:
			logging.info('Cache hit: key = ' + cache_key)
			
		return data
		
	#
	# Generate a key for the given query
	# The mechanism to generate the key is kind of brute, but it seems to work
	#
	def _generate_key_for_query(self, limit, bookmark):
		import pickle
		import md5
		
		return("cachedquery:" + md5.new(pickle.dumps(self) + str(limit) + str(bookmark)).hexdigest())
		