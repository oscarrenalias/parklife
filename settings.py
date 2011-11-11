# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under GNU General Public License version 3:
# http://www.gnu.org/licenses/gpl-3.0.txt
#

import logging
import app
import webapp2
from google.appengine.ext.webapp import util
from app.models.config import Config
from django import newforms as forms
from forms import Forms as parklifeforms
from google.appengine.ext import ereporter
from core import BaseHandler

class UserSettingsForm(forms.Form):
	# TODO: is there any way to keep this shorter?
	twitter_user = forms.CharField(required=False, label='Twitter user', widget=forms.widgets.TextInput(attrs={'size':60}))
	delicious_user = forms.CharField(required=False, label='Delicious user', widget=forms.widgets.TextInput(attrs={'size':60}))
	delicious_password = forms.CharField(required=False, label='Delicious password', widget=forms.widgets.PasswordInput(attrs={'size':60}))
	youtube_user = forms.CharField(required=False, label='YouTube user', widget=forms.widgets.TextInput(attrs={'size':60}))	
	google_reader_feed = forms.CharField(required=False, label='Google Reader shared items RSS feed', widget=forms.widgets.TextInput(attrs={'size':60}))		
	picasa_user = forms.CharField(required=False, label='Picasa user', widget=forms.widgets.TextInput(attrs={'size':60}))
	pinboard_user = forms.CharField(required=False, label='Pinboard user', widget=forms.widgets.TextInput(attrs={'size':60}))
	pinboard_password = forms.CharField(required=False, label='Pinboard password', widget=forms.widgets.PasswordInput(attrs={'size':60}))
	instagram_token = forms.CharField(required=False, label='Instagram OAuth token', widget=forms.widgets.TextInput(attrs={'size':60}))

#
# updates the twitter source
#
class UserSettings(BaseHandler):

	def get(self):	
		self.writeResponse( 'settings.html', { 'form': UserSettingsForm(Config.getAllKeysAsDictionary())})
		
	def post(self):

		form = UserSettingsForm( self.request )		
		if form.is_valid():		
			# get the values from the request and save them to the database
			Config.setKeysFromDictionary(form.clean_data)
		
			self.writeResponse( 'settings.html', { 
				'form': UserSettingsForm(Config.getAllKeysAsDictionary()), 
				'message': 'Settings saved successfully'
			})
		else:
			# form not valid, must show again with the errors
			self.writeResponse( 'settings.html', { 
				'form': form,
				'message': 'There were some errors'
			})

class AdminMaintenance(BaseHandler):
	def get(self):
		self.writeResponse( 'admin_maintenance.html' )

class DoAdminMaintenance(BaseHandler):
	def get(self, op):
		if op == "empty":
			# empty the data store
			from app.models.entry import Entry
			# it's a bit crude but it works :)
			data = Entry().all().fetch(1000)
			total = 0
			for entry in data:
				total += 1
				entry.delete()

			message = str(total) + ' entries deleted'
		else:
			message = 'Unknown operation'

		self.writeResponse( 'admin_maintenance.html', { 'message': message } )

ereporter.register_logger()	
logging.getLogger().setLevel(logging.DEBUG)		
	
application = webapp2.WSGIApplication([
	('/admin/settings', UserSettings), 
	('/admin/maintenance', AdminMaintenance), 
	('/admin/maintenance/(.*)', DoAdminMaintenance)],
	debug=True)