#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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