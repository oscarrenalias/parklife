from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.twitter import Twitter
from app.dateutil.parser import *
import logging

class TwitterSource(Source):
	
	def TwitterSource(self):
		self.source_id = 'twitter'
		
	def getAll(self):
		# fetch all tweets, up to 3200 as per the current API restrictions
		# maximum amount of records per page is 200
		print 'TwitterSource.getAll not implemented'
		
	#
	# returns true if an entry with the same twitter id already exists
	#
	def isDuplicate( self, twitter_id ):
		query = Entry.gql( 'WHERE external_id = :external_id AND source = :source', external_id = str(twitter_id), source = 'twitter' )
		value = False;
		if query.count() > 0: 
			value = True

		logging.debug( 'duplicate check: ' + str(twitter_id) + ' result: ' + str(value))
		return value

	# 
	# return the Entry object that corresponds to the newest tweet
	# REturns None if none is found
	#
	def getNewestTweet(self):
		query = Entry.gql( 'WHERE source = :source ORDER BY external_id DESC', source='twitter')
		if query.count() == 0:
			return None
			
		# can you do this?
		return(query.fetch(1)[0])

	def getLatest(self):

		# get latest entries only
		# retrieve the twitter user
		c = Config()
		twitter_user = c.getKey('twitter_user')
		
		# quit right away if no twitter user has been provided
		if twitter_user == None:
			raise Exception( 'Twitter username missing' )		

		twitter = Twitter()
		
		# retrieve the newest tweet, if any
		newest_tweet = self.getNewestTweet()
		if newest_tweet == None:
			# get everything
			logging.debug('no newest tweet found - requesting all')
			statuses = twitter.statuses.user_timeline(user=twitter_user)			
		else:
			# get only tweets with an id higher than the newest one
			logging.debug('requesting tweets with id greater than ' + str(newest_tweet.external_id))			
			statuses = twitter.statuses.user_timeline(user=twitter_user,since_id=newest_tweet.external_id)
			
		return self._saveTweets( statuses )

	def _saveTweets( self, statuses ):	
		total = 0
		for s in statuses:
			# create Entry objects out of tweets, but we'll be careful not to add duplicates
			
			# is the entry a duplicate?
			logging.debug( 'processing entry ' + str(s['id']))
			if self.isDuplicate( s['id'] ) == True:
				logging.debug( 'Skipping entry with id ' + str(s['id']) + ' because it is duplicate' )
			else:
				e = Entry(external_id = str(s['id']),
				source = 'twitter',
				text = s['text'],
				url = 'http://twitter.com/' + str(s['user']['screen_name'])+'/statuses/' + str(s['id']) )
				e.created = parse(s['created_at'])
				e.put()
				total = total+1
			
		# return the number of rows processed
		return total;
			

	def getLastUpdateDate(self):
		print( 'getLastUpdateDate' )

	def getLastUpdateExternalId(self):
		print( 'getLastUpdateDate' )		