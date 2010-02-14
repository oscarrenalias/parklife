from google.appengine.ext import db

class Config(db.Model):

	# twitter settings
	config_key = db.StringProperty()	
	value = db.StringProperty()
	
	def getKey(key):
		query = Config.gql( 'WHERE config_key = :config_key', config_key = key )
		# keys are unique, so we can assume that there will only be one result
		results = query.fetch(1)
		if query.count() == 0:
			return None
			
		result = results.pop()
		return result.value
		
	def setKey(key, value):
		query = Config.gql( 'WHERE config_key = :config_key', config_key = key )
		settings = query.get()
		if settings == None:
			settings = Config()
			
		settings.config_key = key
		settings.value = value
		settings.put()		
			
	getKey = staticmethod(getKey)
	setKey = staticmethod(setKey)