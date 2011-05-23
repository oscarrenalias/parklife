from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.delicious import *
from app.dateutil.parser import *
import logging

class DeliciousSource(Source):
	
	source_id = 'delicious'
	
	FETCH_ALL_POST_COUNT = 100
	
	def DeliciousSource(self):
		pass
	
	def getAll(self):
		# fetches all delicious links
		#def posts_all(self, tag="", start=None, results=None, fromdt=None,		
		d = DeliciousAPI( Config.getKey( 'delicious_user'), Config.getKey( 'delicious_password' ))
		
		try:
			posts = d.posts_all(results=self.FETCH_ALL_POST_COUNT)
		except PyDeliciousUnauthorized: 
			# log the error but still throw the exception upwards
			logging.error( 'User ' + str(Config.getKey('delicious_user')) + ' could not log into delicious.com account' )
			raise PyDeliciousUnauthorized
		
		return posts
		
	def getLatest(self):
		
		latestLink = self.getMostRecentEntry()
		if latestLink == None:
			# should we fetch them all?
			logging.debug( 'Fetching all delicious links because there is none in the database')
			return self.getAll()

		logging.debug( 'Doing a delta update' )
		
		# check the date of the most recent link
		most_recent = self.getMostRecentLink()
		date = most_recent.created
		# and make a API call to obtain all the links since that one
		d = DeliciousAPI( Config.getKey('delicious_user'), Config.getKey('delicious_password'))
		logging.debug('Date of the most recent link is ' + str(most_recent.created))
		posts = d.posts_all(fromdt=most_recent.created.strftime("%Y-%m-%dT%H:%M:%SZ"))
		
		return posts
	
	def toEntry(self, post):
		e=Entry()
		e.external_id = post['hash']
		e.url = post['href']
		e.title = post['description']
		e.text = post['extended']
		e.source = 'delicious'
		e.created = parse( post['time'] )
		if post['tag'] != '':
			e.tags = post['tag'].split(' ')	
		else:
			e.tags = []

		return e