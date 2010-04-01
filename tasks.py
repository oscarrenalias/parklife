#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under GNU General Public License version 3:
# http://www.gnu.org/licenses/gpl-3.0.txt
#

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

#
# updates the twitter source
#
class UpdateSources( webapp.RequestHandler ):
	
	def get(self, source):	
		total = 0		
		
		if source == "twitter":
			from app.source.twitter import TwitterSource
			source_class = TwitterSource()
		elif source == "delicious":
			from app.source.delicious import DeliciousSource
			source_class = DeliciousSource()
		elif source == "youtube":
			from app.source.youtube import YouTubeSource		
			source_class = YouTubeSource()
		elif source == "googlereader":
			from app.source.googlereader import GoogleReaderSource		
			source_class = GoogleReaderSource()
		else:
			raise Exception('unrecognized source')
			
		# load the latest data from the soruce
		logging.info('Updating source: ' + source)				
		total = source_class.getLatest()			
		# and reset the data cache if we at least added one new entry
		if total > 0:
			logging.info('Resetting query cache after importing ' + str(total) + ' entries from source \'' + source + '\'')
			from google.appengine.api import memcache
			memcache.flush_all()
		
		logging.debug( 'source ' + str(source) + ': ' + str(total) + ' entries updated' )

def main():
  logging.getLogger().setLevel(logging.DEBUG)		
	
  application = webapp.WSGIApplication([('/tasks/update/(.*)', UpdateSources)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()