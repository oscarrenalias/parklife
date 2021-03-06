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
from app.view.view import View
from defaults import Defaults
from google.appengine.ext.db import BadKeyError
from app.forms.forms import forms
from app.core import BaseHandler

#
# form object for the new blog entry
#	
class EntryForm(forms.Form):
	title = forms.CharField(label='Title for the blog post', seq=1, widget=forms.widgets.TextInput(attrs={'size':60, 'class': 'full-width'}))
	text = forms.CharField(label='Text for the blog post', seq=2, widget=forms.widgets.TextArea(attrs={'rows': 14, 'cols': 60, 'class': 'mceEditor full-width' }))
	tags = forms.CharField(required=False,label='Tags', seq=3, widget=forms.widgets.TextInput(attrs={'size':60, 'class': 'full-width'}))
	lat = forms.CharField(required=False, seq=4, widget=forms.widgets.HiddenInput(attrs={'size':15}))
	lng = forms.CharField(required=False, seq=5, widget=forms.widgets.HiddenInput(attrs={'size':15}))

class BlogHandler(BaseHandler):	

	def get(self):	
		# display the form
		self.writeResponse( 'new_blog_post.html', { 'form': EntryForm().render() } )

	# this code is only called if for some reason javascript isn't available
	def post(self):
		form = EntryForm( self.request.POST )
		if form.is_valid():
			# validation successful, we can save the data
			e = Entry()
			print(form.clean_data)
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
			self.writeResponse( 'new_blog_post.html', { 'form': form.render() } )
			
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
			self.writeResponse('new_blog_post.html', { 
				'entry': entry, 
				'entry_id': entry.key(), 
				'form': EntryForm(instance=entry).render() 
			})		
			
#
# RESTful handler for entries. Supports creation (POST), deletion (DELETE),
# updates (UPDATE) and retrieval (GET) of entries
# Results are always returned as JSON responses
#
class BaseJSonHandler(BaseHandler):
	def writeResponse(self, data):
		responseContent, contentType = View(None, self.request).render(data, force_renderer='json')
		self.response.headers['Content-type'] = contentType
		self.response.out.write(responseContent)


class EntryHandler(BaseJSonHandler):
	
	#
	# returns an entry
	#
	def get(self, entry_id):
		e = Entry.get( entry_id )
		
		if e == None:
			# entry not found
			self.writeResponse({'error': True, 'message': 'Entry not found'})
		else:	
			self.writeResponse({'error': False, 'entry': e, 'entry_id': entry_id})
		
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
			view_data = {
				'message': 'New blog entry added successfully. <a href="%s">Link to the entry</a>.' % e.permalink(), 
				'error': False,
				'entry_link': e.permalink(),							
				'entry': e
			}
			self.writeResponse(view_data)

		else:
			# form not valid, must show again with the errors
			data = { 'error': True, 'errors': {}}
			# (the Form object is actually iterable)
			for field in form:
				if field.errors:
					data['errors'][field.name] = field.errors

			self.writeResponse(data)

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
			
		form = EntryForm( self.request.POST )
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
		self.writeResponse(data)
			
	#
	# create or update an entry
	#
	def post(self, entry_id):
		form = EntryForm( self.request.POST )
		
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
			self.writeResponse({'error': True, 'message': 'Entry not found'})
		else:
			# otherwise, mark it as deleted and return success
			e.deleted = True
			e.put()
			
			# reset the data cache since there's been some changes
			from google.appengine.api import memcache
			memcache.flush_all()		
			
			self.writeResponse({'error': False, 'message': 'Entry successfully deleted', 'entry_id': entry_id})

logging.getLogger().setLevel(logging.DEBUG)	
	
application = webapp2.WSGIApplication([
	('/admin/blog', BlogHandler), 
	('/admin/edit/(.*)', EditEntryHandler), 
	('/service/entry/(.*)', EntryHandler)], 
	debug=True)