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
from app.view.view import View
from defaults import Defaults
from app.pager.pager import PagerQuery
from google.appengine.ext import db

class MainHandler(webapp.RequestHandler):	

	def get(self ):	

	    # Build a paginated query.
		query = PagerQuery(Entry).order('-created')

	    # Fetch results for the current page and bookmarks for previous and next
	    # pages.
		bookmark = self.request.get( 'p' )
		prev, entries, next = query.fetch( Defaults.POSTS_PER_PAGE, bookmark ) 

		if self.request.get( 'f') == 'json':
			import app.simplejson as json
			self.response.out.write( json.dumps( { 'payload': [entry.__dict__ for entry in entries], 'prev': prev, 'next': next } ))
		else:
			self.response.out.write(View.render('index.html', {'entries': entries, 'prev': prev, 'next': next }))
			
class EntryHandler(webapp.RequestHandler):
	
	def get(self, entry_slug):
		
		# see if we can find the entry
		entry = Entry.all().filter('slug =', entry_slug ).get()
		
		# entry not found
		if entry == None:
			self.response.out.write( View.render ('error.html', { 'message': 'Entry could not be found '} ))
			return
			
		# if found, display it	
		self.response.out.write( View.render ('entry.html', { 'entry': entry }))
		
class SourceHandler(webapp.RequestHandler):
	
	def get(self, source):
		
		query = PagerQuery(Entry).filter('source =', source).order('-created')
		bookmark = self.request.get( 'p' )
		prev, entries, next = query.fetch( Defaults.POSTS_PER_PAGE, bookmark ) 

		if self.request.get( 'f') == 'json':
			import app.simplejson as json
			self.response.out.write( json.dumps( { 'payload': [entry.__dict__ for entry in entries], 'prev': prev, 'next': next } ))
		else:
			self.response.out.write(View.render('index.html', {'entries': entries, 'prev': prev, 'next': next }))		

def main():
  logging.getLogger().setLevel(logging.DEBUG)	
	
  application = webapp.WSGIApplication([('/', MainHandler), ('/entry/(.*)', EntryHandler ), ('/source/(.*)', SourceHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()