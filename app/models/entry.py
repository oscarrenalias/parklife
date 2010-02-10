from google.appengine.ext import db
import datetime

class Entry(db.Model):
	# creation date
	created = db.DateTimeProperty()
	
	# external id - can be used to store the source's own identifier, e.g
	# twitter's own tweet id
	external_id = db.StringProperty()
	
	# source identifier/name
	source = db.StringProperty()
	
	# text of the entry
	text = db.TextProperty()
	
	# is there a link pointing to this url?
	url = db.LinkProperty()
	
	# tags, for those sources that support them
	tags = db.StringProperty()
	
	# 
	# returns the 20 most recent entries
	#
	def getRecent():
		query = db.GqlQuery( "SELECT * FROM Entry ORDER BY created DESC" )
		results = query.fetch( 20 )
		
		return( results )
		
	getRecent = staticmethod( getRecent )
	