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
from app.models.config import Config
#from django import forms
from core import BaseHandler
from abc import ABCMeta

class forms:

	class CharField:
		def __init__(self, required, label, widget):
			self.required = required
			self.label = label
			self.widget = widget

	class widgets:

		class BaseWidget:
			__metaclass__ = ABCMeta

			def __init__(self, attrs):
				self.attrs = attrs

			def render(self):
				raise("Method must be implemented by child classes")

		class TextInput(BaseWidget):
			pass

		class PasswordInput(BaseWidget):
			pass			

	class Form:
		def __init__(self, values):
			pass

		def render(self):
			"form"


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

logging.getLogger().setLevel(logging.DEBUG)		
	
application = webapp2.WSGIApplication([
	('/admin/settings', UserSettings), 
	('/admin/maintenance', AdminMaintenance), 
	('/admin/maintenance/(.*)', DoAdminMaintenance)],
	debug=True)