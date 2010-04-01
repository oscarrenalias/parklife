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
			logging.debug('updating twitter')		
			twitterSource = TwitterSource()
			total = twitterSource.getLatest()
		elif source == "delicious":
			from app.source.delicious import DeliciousSource						
			logging.debug('updating delicious')
			deliciousSource = DeliciousSource()
			total = deliciousSource.getLatest()
		elif source == "youtube":
			from app.source.youtube import YouTubeSource						
			logging.debug('updating youtube')
			ytSource = YouTubeSource()
			total = ytSource.getLatest()			
		elif source == "googlereader":
			from app.source.googlereader import GoogleReaderSource						
			logging.debug('updating google reader')
			grSource = GoogleReaderSource()
			total = grSource.getLatest()			
		else:
			raise Exception('unrecognized source')
		
		logging.debug( 'source ' + str(source) + ': ' + str(total) + ' entries updated' )

def main():
  logging.getLogger().setLevel(logging.DEBUG)		
	
  application = webapp.WSGIApplication([('/tasks/update/(.*)', UpdateSources)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()