#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under GNU General Public License version 3:
# http://www.gnu.org/licenses/gpl-3.0.txt
#

import app
import logging
import webapp2
from app.utils.classhelper import ClassHelper

#
# This is the controller class that receives requests from the cron and triggers
# the source updates as required
#
class UpdateSources( webapp2.RequestHandler ):
	
	#sources = {
	#		'twitter': TwitterSource,
	#		'delicious': DeliciousSource,
	#		'youtube': YouTubeSource,
	#		'picasa': PicasaSource,
	#		'googlereader': GoogleReaderSource,
	#		'pinboard': PinboardSource
	#}
	sources = { 
			"twitter": "TwitterSource", 
			"delicious": "DeliciousSource",
			"youtube": "YouTubeSource", 
			"picasa": "PicasaSource", 
			"googlereader": "GoogleReaderSource", 
			"pinboard": "PinboardSource",
			"instagram": "InstagramSource" 
	} 

	
	def get(self, source):	
		total = 0
		
		if source in self.sources:
			className = "app.source." + source + "." + self.sources[source]
			source_class = ClassHelper.get_class(className)()
		else:
			raise Exception("Unknown source")		
				
		# load the latest data from the soruce
		logging.info('Updating source: ' + source)				
		#total = source_class.getLatest()
		total = source_class.update()			
		# and reset the data cache if we at least added one new entry
		if total > 0:
			logging.info('Resetting query cache after importing ' + str(total) + ' entries from source \'' + source + '\'')
			from google.appengine.api import memcache
			memcache.flush_all()
		
		logging.debug( 'source ' + str(source) + ': ' + str(total) + ' entries updated' )

	
application = webapp2.WSGIApplication([('/tasks/update/(.*)', UpdateSources)], debug=True)