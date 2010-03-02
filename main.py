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
from app.models.config import Config
from app.view.view import View
from defaults import Defaults
from app.pager.pager import PagerQuery
from google.appengine.ext import db
from google.appengine.ext.db import BadKeyError

class MainHandler(webapp.RequestHandler):	

	def get(self ):	

	    # Build a paginated query.
		query = PagerQuery(Entry).filter('deleted = ', False).order('-created')

	    # Fetch results for the current page and bookmarks for previous and next
	    # pages.
		bookmark = self.request.get( 'p' )
		prev, entries, next = query.fetch( Defaults.POSTS_PER_PAGE, bookmark ) 
		
		data = {'entries': entries, 'prev': prev, 'next': next }

		self.response.out.write(View(self.request).render('index.html', data ))
			
class EntryHandler(webapp.RequestHandler):
	
	def get(self, entry_slug):
		
		# see if we can find the entry by slug
		entry = Entry.all().filter('slug =', entry_slug ).filter('deleted = ', False).get()
		# entry not found, let's try by id
		if entry == None:
			try: 
				entry = Entry.get(entry_slug)
			except BadKeyError:
				entry = None
				
			if entry == None:
				self.response.out.write( View(self.request).render ('error.html', { 'message': 'Entry could not be found '} ))
				return
					
		# check if we need to return the entire body or just the html code for the entry
		if self.request.get('b'):
			template = 'entry_data.html'
		else:
			template = 'entry.html'
			
		# if found, display it	
		self.response.out.write( View(self.request).render(template, { 'entry': entry } ))
		
class SourceHandler(webapp.RequestHandler):
	
	def get(self, source):
		
		query = PagerQuery(Entry).filter('source =', source).filter('deleted = ', False).order('-created')
		bookmark = self.request.get( 'p' )
		prev, entries, next = query.fetch( Defaults.POSTS_PER_PAGE, bookmark ) 
		
		from app.utils import StringHelper
		view_data = {
			'entries': entries, 
			'prev': prev, 
			'next': next,
			'source': StringHelper.remove_html_tags(source)
		}

		self.response.out.write(View(self.request).render('index.html', view_data ))		
			
class TagHandler(webapp.RequestHandler):
	
	def get(self, tag):
			query = PagerQuery(Entry).filter('tags = ', tag).filter('deleted = ', False).order( '-created' )
			bookmark = self.request.get( 'p' )
			prev, entries, next = query.fetch( Defaults.POSTS_PER_PAGE, bookmark )

			from app.utils import StringHelper			
			view_data = {
				'entries': entries, 
				'prev': prev, 
				'next': next,
				'tag': StringHelper.remove_html_tags(tag)
			}			
			
			self.response.out.write(View(self.request).render('index.html', view_data ))

def main():

	
	logging.getLogger().setLevel(logging.DEBUG)	
	
	application = webapp.WSGIApplication([ ('/', MainHandler), ('/entry/(.*)', EntryHandler ), ('/source/(.*)', SourceHandler), ('/tag/(.*)', TagHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
  main()