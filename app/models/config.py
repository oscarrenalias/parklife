from google.appengine.ext import db
import logging

class Config(db.Model):

	# class attributes
	config_key = db.StringProperty()	
	value = db.StringProperty()
	
	@staticmethod
	def getKey(key):
		query = Config.gql( 'WHERE config_key = :config_key', config_key = key )
		# keys are unique, so we can assume that there will only be one result
		results = query.fetch(1)
		if query.count() == 0:
			return None
			
		result = results.pop()
		return result.value
		
	@staticmethod
	def setKey(key, value):
		query = Config.gql( 'WHERE config_key = :config_key', config_key = key )
		settings = query.get()
		if settings == None:
			settings = Config()
			
		settings.config_key = key
		settings.value = value
		settings.put()		
		
	#
	# Retrieves all configuration keys from the Config table and returns then
	# as a dictionary
	#
	@staticmethod
	def getAllKeysAsDictionary():
		return(dict(map(lambda i:(i.config_key, i.value), Config.all())))
	
	#
	# sets the given keys from a dictionary
	#
	@staticmethod
	def setKeysFromDictionary(keys):
		dict2list = lambda dic: [(k, v) for (k, v) in dic.iteritems()]
		map(lambda c: Config.setKey(c[0], c[1]), dict2list(keys))