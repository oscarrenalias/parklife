from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.delicious import *
from app.dateutil.parser import *
import logging

class DeliciousSource(Source):
	
	def DeliciousSource(self):
		self.source_id = 'delicious'
	
	#
	# returns the Entry object point to the delicious link that was most recently fetched
	#	
	def getMostRecentLink(self):
		query = Entry.gql( 'WHERE source = :source ORDER BY created DESC', source='delicious')
		if query.count() == 0:
			return None
			
		# can you do this?
		return(query.fetch(1)[0])		
		
	def getAll(self):
		# fetches all delicious links
		#def posts_all(self, tag="", start=None, results=None, fromdt=None,		
		d = DeliciousAPI( Config.getKey( 'delicious_user'), Config.getKey( 'delicious_password' ))
		
		try:
			posts = d.posts_all(results=100)
		except PyDeliciousUnauthorized: 
			# log the error but still throw the exception upwards
			logging.error( 'User ' + str(Config.getKey('delicious_user')) + ' could not log into delicious.com account' )
			raise PyDeliciousUnauthorized
		
		total = self.__processLinks(posts)
		
		logging.debug( 'delicious updated ' + str(total) + ' links' )
		
		return total
		
	def getLatest(self):
		
		latestLink = self.getMostRecentLink()
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
		
		return self.__processLinks(posts)
			
	def __processLinks(self, posts):		
		# process all data received from delicious
		total = 0
		added = 0
		for post in posts['posts']:
			total = total + 1
			if self.isDuplicate(post['hash'], 'delicious') == False:
				# only persist if not duplicate
				e=Entry()
				e.external_id = post['hash']
				e.url = post['href']
				e.title = post['description']
				e.text = post['extended']
				e.source = 'delicious'
				e.created = parse( post['time'] )
				e.tags = post['tag']				
				
				e.put()
				
				added = added + 1
			else:
				logging.debug( 'Skipping link ' + post['hash'] + ' because it is duplicate')
		
		logging.debug('Processed ' + str(total) + ' links, ' + str(added) + ' updated' )
		return added