from google.appengine.ext import db

class Config(db.Model):

	# twitter settings
	config_key = db.StringProperty()	
	config_value = db.StringProperty()
	
	def getKey(self, key):
		query = self.gql( 'WHERE config_key = :config_key', config_key = key )
		# keys are unique, so we can assume that there will only be one result
		results = query.fetch(1)
		result = results.pop()
		return result.config_value