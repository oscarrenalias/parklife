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

import sys
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from app.models.entry import Entry
from app.source.delicious import DeliciousSource
from app.twitter import Twitter
from app.models.config import Config
from app.source.twitter import TwitterSource
import os
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):

  def get(self):
	
	# 
	# retrieve the most recent entries
	#
	entries = Entry.getRecent()
	
	template_values = { 'entries': entries }
	
	path = os.path.join(os.path.dirname(__file__), 'app/templates/index.html')
	self.response.out.write(template.render(path, template_values))
	
#
# updates the twitter source
#
class UpdateTwitter( webapp.RequestHandler ):
	
	def get(self):
		print 'updating twitter'
		
		twitterSource = TwitterSource()
		total = 0
		total = twitterSource.getLatest()
		
		print str(total) + ' entries updated'

def main():
	
  
  logging.getLogger().setLevel(logging.DEBUG)	
	
  application = webapp.WSGIApplication([('/', MainHandler), ('/update/twitter', UpdateTwitter), ('/update/twitter/all', UpdateTwitter) ],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()