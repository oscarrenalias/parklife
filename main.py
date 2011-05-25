#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under GNU General Public License version 3:
# http://www.gnu.org/licenses/gpl-3.0.txt
#

import sys
import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from app.models.entry import Entry
from app.models.config import Config
from app.view.view import View
from defaults import Defaults
from app.pager.pager import PagerQuery
from app.pager.cachedquery import CachedQuery
from app.pager.pagedquery import PagedQuery
from google.appengine.ext import db
from google.appengine.ext.db import BadKeyError
from google.appengine.ext import ereporter
from core import BaseHandler

class MainHandler(BaseHandler):

	def get(self ):	

	    # Build a paginated query.
		query = PagedQuery(Entry).filter('deleted = ', False).order('-created')
		
		if Defaults.TWITTER_IGNORE_AT_REPLIES:
			query = query.filter('twitter_reply = ', False )

	    # Fetch results for the current page and bookmarks for previous and next
	    # pages.
		page = self.getCurrentPage()
		prev, entries, next = query.fetch( page, Defaults.POSTS_PER_PAGE ) 
		
		data = {'entries': entries, 'prev': prev, 'next': next }

		self.writeResponse('index.html', data )
		
			
class EntryHandler(BaseHandler):
	
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
		self.writeResponse(template, { 'entry': entry } )
		
class SourceHandler(BaseHandler):
	
	def get(self, source):
		
		query = PagedQuery(Entry).filter('source =', source).filter('deleted = ', False).order('-created')
		
		if Defaults.TWITTER_IGNORE_AT_REPLIES:
			query = query.filter('twitter_reply = ', False )		
		
		page = self.getCurrentPage()
		prev, entries, next = query.fetch( page, Defaults.POSTS_PER_PAGE ) 
		
		from app.utils import StringHelper
		view_data = {
			'entries': entries, 
			'prev': prev, 
			'next': next,
			'source': StringHelper.remove_html_tags(source)
		}

		self.writeResponse('index.html', view_data )		
			
class TagHandler(BaseHandler):
	
	def get(self, tag):
		query = CachedQuery(Entry).filter('tags = ', tag).filter('deleted = ', False).order( '-created' )
			
		if Defaults.TWITTER_IGNORE_AT_REPLIES:
			query = query.filter('twitter_reply = ', False )			
			
		page = self.getCurrentPage()
		prev, entries, next = query.fetch( page, Defaults.POSTS_PER_PAGE ) 

		from app.utils import StringHelper			
		view_data = {
			'entries': entries, 
			'prev': prev, 
			'next': next,
			'tag': StringHelper.remove_html_tags(tag)
		}			
			
		self.writeResponse('index.html', view_data )
			
class PlacesHandler(BaseHandler):
	
	def get(self):
		# this action generates different content depending on how it is called
		if self.request.get('f') == 'json':
			# select those entries that have location data
			query = Entry.gql('WHERE lat != :lat AND deleted = :deleted', lat=None, deleted=False)
			view_data = { 'entries': query }
		else:
			view_data = {}

		self.writeResponse('places.html', view_data)
		
class NotFoundPageHandler(BaseHandler):
	def get(self):
		self.error(404)
		self.writeResponse('error.html', {'message': 'The page could not be found'} )

def main():
	ereporter.register_logger()
	logging.getLogger().setLevel(logging.DEBUG)	
	
	application = webapp.WSGIApplication(
		[ 
			('/', MainHandler), 
			('/entry/(.*)', EntryHandler ), 
			('/source/(.*)', SourceHandler), 
			('/tag/(.*)', TagHandler), 
			('/places', PlacesHandler), 
			('/.*', NotFoundPageHandler)			
		], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
  main()