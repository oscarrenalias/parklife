from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.twitter import Twitter
from app.dateutil.parser import *
from app.utils import Utils
import logging

class TwitterSource(Source):
	
	# source identifier for this source
	source_id = 'twitter'
	
	# maximum number of entries to fetch if none is found in the database
	FETCH_ALL_MAX_ENTRIES = 40
	
	def TwitterSource(self):
		pass
		
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
		newest_tweet = self.getMostRecentEntry()
		if newest_tweet == None:
			# get everything
			logging.debug('no newest tweet found - requesting all')
			statuses = twitter.statuses.user_timeline(user=twitter_user,count=self.FETCH_ALL_MAX_ENTRIES)			
		else:
			# get only tweets with an id higher than the newest one
			logging.debug('requesting tweets with id greater than ' + str(newest_tweet.external_id))			
			statuses = twitter.statuses.user_timeline(user=twitter_user,since_id=newest_tweet.external_id,count=40)
			
		return(statuses)
	
	def toEntry(self, status):
		from app.utils import StringHelper			
		e = Entry(external_id=str(status['id']),
		source = self.source_id,
		text = Utils.links_to_anchors(Utils.twitpic_to_img(status['text'])),
		title = StringHelper().remove_new_lines(status['text']),
		url='http://twitter.com/' + str(status['user']['screen_name']) + '/statuses/' + str(status['id']))
		e.created = parse(status['created_at'])
		
		# extract the tags
		e.tags = StringHelper().extract_twitter_tags(status['text'])
		
		# process the location coordinates if they're available
		if status['coordinates'] != None:
			e.lat = str(status['coordinates']['coordinates'][1])
			e.lng = str(status['coordinates']['coordinates'][0])	
			
		# is this entry a reply-to?
		logging.debug(e.text[0])
		e.twitter_reply = (e.text[0] == '@')
		
		return(e)