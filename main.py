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
from app.pager.pagedquery import PagedQuery
from google.appengine.ext import db
from google.appengine.ext.db import BadKeyError
from google.appengine.ext import ereporter
from core import BaseHandler
from utils.classhelper import DynamicDispatcherMixin

class NotFoundPageHandler(BaseHandler):
	def get(self):
		self.error(404)
		self.writeResponse('error.html', {'message': 'The page could not be found'} )

# 
# This request handler is reponsible for handling all kinds of entry points to the site content, instead of
# splitting each URL into its own request handler.
# It uses some dynamic method calls to route execution logic to a specific method based on the request and URL
# parameters
#
class FrontHandler(BaseHandler, DynamicDispatcherMixin):
	def get(self, *params):
		# do some basic stuff first
		self.page = self.getCurrentPage()		
		
		if len(params) == 0:
			template, view_data = self.default()
			self.writeResponse(template, view_data)
		else:	
			# dynamically route the method call (stored in params[0] to the correct method with the remaining parameters
			if self.has_method(params[0]):
				template, view_data = self.call_method(params[0], *params[1:])
				self.writeResponse(template, view_data)
			
	def default(self):
		query = self.getEntryQuery()		
		prev, entries, next = query.fetch( self.page, Defaults.POSTS_PER_PAGE ) 		
		data = {'entries': entries, 'prev': prev, 'next': next }
		return 'index.html', data		
		
	def tag(self, tag):
		query = self.getEntryQuery({'tags = ':tag})			
		prev, entries, next = query.fetch( self.page, Defaults.POSTS_PER_PAGE ) 
		from app.utils import StringHelper			
		view_data = { 'entries': entries, 'prev': prev, 'next': next, 'tag': StringHelper.remove_html_tags(tag) }		
		return 'index.html', view_data
		
	def source(self, source):
		query = self.getEntryQuery({'source =':source})		
		prev, entries, next = query.fetch( self.page, Defaults.POSTS_PER_PAGE ) 		
		from app.utils import StringHelper
		view_data = { 'entries': entries, 'prev': prev, 'next': next, 'source': StringHelper.remove_html_tags(source) }
		return 'index.html', view_data
		
	def entry(self, entry_slug):
		
		# see if we can find the entry by slug
		entry = Entry.all().filter('slug =', entry_slug ).filter('deleted = ', False).get()
		#entry = self.getEntryQuery({'slug = ': entry_slug}).get()
		# entry not found, let's try by id
		if entry == None:
			try: 
				entry = Entry.get(entry_slug)
			except BadKeyError:
				entry = None
				
			if entry == None:
				self.response.out.write( View(self.request).render ('error.html', { 'message': 'Entry could not be found '} ))
				return
					
		# if found, display it
		return 'entry.html', { 'entry': entry } 	
		
	def places(self):
		# this action generates different content depending on how it is called
		view_data = {}
		if self.request.get('f') == 'json':
			# select those entries that have location data
			query = Entry.gql('WHERE lat != :lat AND deleted = :deleted', lat=None, deleted=False)
			view_data = { 'entries': query }
				
		return 'places.html', view_data
		
def main():
	ereporter.register_logger()
	logging.getLogger().setLevel(logging.DEBUG)	
	
	application = webapp.WSGIApplication(
		[ 
			('/', FrontHandler), 
			('/(entry)/(.*)', FrontHandler ), 
			('/(source)/(.*)', FrontHandler), 
			('/(tag)/(.*)', FrontHandler),
			('/(test)/(.*)', FrontHandler), 
			('/(places)', FrontHandler), 
			('/.*', NotFoundPageHandler)			
		], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
  main()