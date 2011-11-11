#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under the General Public License version 3


import sys
import logging
import webapp2
import app
from app.models.entry import Entry
from app.models.config import Config
from view.view import View
from defaults import Defaults
from django import newforms as forms
from google.appengine.ext.db import BadKeyError
from google.appengine.ext.db import djangoforms
from forms import Forms as parklifeforms
from core import BaseHandler

#
# form object for the new blog entry
#	
class EntryForm(djangoforms.ModelForm):
	
	title = forms.CharField(label='Title for the blog post', widget=forms.widgets.TextInput(attrs={'size':60, 'class': 'full-width'}))
	text = forms.CharField(label='Text for the blog post', widget=forms.widgets.Textarea(attrs={'rows': 14, 'cols': 60, 'class': 'mceEditor full-width' }))
	tags = forms.CharField(required=False,label='Tags', widget=forms.widgets.TextInput(attrs={'size':60, 'class': 'full-width'}))
	lat = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={'size':15}))
	lng = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={'size':15}))
	
	class Meta:			
		model = Entry
		fields = [ 'title', 'text', 'tags', 'lat', 'lng' ]
	

class BlogHandler(BaseHandler):	

	def get(self):	
		# display the form
		self.writeResponse( 'new_blog_post.html', { 'form': EntryForm() } )

	# this code is only called if for some reason javascript isn't available
	def post(self):
		form = EntryForm( self.request )
		if form.is_valid():
			# validation successful, we can save the data
			e = Entry()
			e.title = form.clean_data['title']
			e.text = form.clean_data['text']
			e.tags = form.clean_data['tags'].split(' ')
			e.lat = form.clean_data['lat']
			e.lng = form.clean_data['lng']
			e.source = 'blog'
			e.put()
			
			# redirect to the main page
			self.redirect( '/' )
		else:
			# form not valid, must show again with the errors
			self.writeResponse( 'new_blog_post.html', { 'form': form } )
			
class EditEntryHandler(BaseHandler):
		
	def get(self, entry_id):
		try:
			entry = Entry.get(entry_id)
		except BadKeyError:
			entry = None
				
		if entry == None:
			self.writeResponse('error.html', { 'message': 'Entry could not be found '} )
		else:			
			# if found, display it	
			self.writeResponse('new_blog_post.html', { 'entry': entry, 'entry_id': entry.key(), 'form':EntryForm(instance=entry) } )		
			
#
# RESTful handler for entries. Supports creation (POST), deletion (DELETE),
# updates (UPDATE) and retrieval (GET) of entries
# Results are always returned as JSON responses
#
class EntryHandler(BaseHandler):
	
	#
	# returns an entry
	#
	def get(self, entry_id):
		e = Entry.get( entry_id )
		
		if e == None:
			# entry not found
			self.response.out.write(View(None, self.request).render( {'error': True, 'message': 'Entry not found'}, force_renderer='json'))
			
		self.response.out.write(View(None, self.request).render( {'error': False, 'entry': e, 'entry_id': entry_id}, force_renderer='json'))	
		
	#
	# add an entry
	#		
	def _addNewEntry(self, form):
		if form.is_valid():
			# validation successful, we can save the data
			e = Entry()
			e.title = form.clean_data['title']
			e.text = form.clean_data['text']
			e.tags = form.clean_data['tags'].split(' ')
			e.lat = form.clean_data['lat']
			if e.lat == "":
				e.lat = None
			e.lng = form.clean_data['lng']			
			if e.lng == "":
				e.lng = None
			e.source = 'blog'
			e.put()
			
			e = Entry.get(e.key())
			
			# reset the data cache since there's new content
			from google.appengine.api import memcache
			memcache.flush_all()			

			# return successful creation
			self.response.out.write( View(None, self.request).render( {
				'message': 'New blog entry added successfully. <a href="%s">Link to the entry</a>.' % e.permalink(), 
				'error': False,
				'entry_link': e.permalink(),				
				'entry': e
			}, force_renderer='json'))

		else:
			# form not valid, must show again with the errors
			data = { 'error': True, 'errors': {}}
			# (the Form object is actually iterable)
			for field in form:
				if field.errors:
					data['errors'][field.name] = field.errors

			self.response.out.write( View(None, self.request).render( data, force_renderer='json'))

	#
	# update an entry
	#			
	def _updateEntry(self, form, entry_id):
		logging.debug("query string: " + self.request.query_string)
		logging.debug("query body: " + self.request.body)
		e = Entry.get( entry_id )
		
		if e == None:
			# entry not found
			self.response.out.write( View(None, self.request).render( {'error': True, 'message': 'Entry not found'}, force_renderer='json'))
			
		form = EntryForm( data=self.request.POST )
		if form.is_valid():
			# validation succesful
			e.title = form.clean_data['title']
			e.text = form.clean_data['text']
			e.tags = form.clean_data['tags'].split(' ')
			e.lat = form.clean_data['lat']
			e.lng = form.clean_data['lng']			
			e.put()
			
			# reset the data cache since there's new content
			from google.appengine.api import memcache
			memcache.flush_all()			
			
			data = {
				'error': False, 
				'entry': e, 
				'entry_id': entry_id,
				'entry_link': e.permalink(),
				'message': 'Entry successfully updated. <a href="%s">Link to the entry</a>.' % e.permalink(),
			}
		else:
			# form not valid, must show again with the errors
			data = { 'error': True, 'errors': {}}
			# (the Form object is actually iterable)
			for field in form:
				if field.errors:
					data['errors'][field.name] = field.errors

		# return the view
		self.response.out.write( View(None, self.request).render( data, force_renderer='json'))			
			
	#
	# create or update an entry
	#
	def post(self, entry_id):
		form = EntryForm( self.request )
		
		if entry_id == None or entry_id == "":
			self._addNewEntry(form)
		else:
			self._updateEntry(form, entry_id)
	
	#
	# deletes an entry
	#
	def delete(self, entry_id):
		e = Entry.get( entry_id )
		
		if e == None:
			# entry not found
			self.response.out.write( View(None, self.request).render({'error': True, 'message': 'Entry not found'}, force_renderer='json'))
			
		# otherwise, mark it as deleted and return success
		e.deleted = True
		e.put()
		
		# reset the data cache since there's been some changes
		from google.appengine.api import memcache
		memcache.flush_all()		
		
		self.response.out.write( View(None, self.request).render({'error': False, 'message': 'Entry successfully deleted', 'entry_id': entry_id}, force_renderer='json'))	

logging.getLogger().setLevel(logging.DEBUG)	
	
application = webapp2.WSGIApplication([
	('/admin/blog', BlogHandler), 
	('/admin/edit/(.*)', EditEntryHandler), 
	('/service/entry/(.*)', EntryHandler)], 
	debug=True)