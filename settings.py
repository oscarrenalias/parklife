#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under GNU General Public License version 3:
# http://www.gnu.org/licenses/gpl-3.0.txt
#

import logging
from app.view.view import View
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from app.models.config import Config
from app.source.twitter import TwitterSource
from django import newforms as forms
from app.forms import Forms as parklifeforms

class UserSettingsForm(forms.Form):
	twitter_user = forms.CharField(required=False, label='Twitter user', widget=forms.widgets.TextInput(attrs={'size':60}))
	delicious_user = forms.CharField(required=False, label='Delicious user', widget=forms.widgets.TextInput(attrs={'size':60}))
	delicious_password = forms.CharField(required=False, label='Delicious password', widget=forms.widgets.PasswordInput(attrs={'size':60}))
	youtube_user = forms.CharField(required=False, label='YouTube user', widget=forms.widgets.TextInput(attrs={'size':60}))	
	google_reader_feed = forms.CharField(required=False, label='Google Reader shared items RSS feed', widget=forms.widgets.TextInput(attrs={'size':60}))		

#
# updates the twitter source
#
class UserSettings( webapp.RequestHandler ):
	
	def get(self):	
		initial_data = {
			'twitter_user': Config.getKey( 'twitter_user' ),
			'delicious_user': Config.getKey( 'delicious_user' ),
			'delicious_password': Config.getKey( 'delicious_password' ),
			'youtube_user': Config.getKey( 'youtube_user' ),
			'google_reader_feed': Config.getKey( 'google_reader_feed' )			
		}
	
		self.response.out.write( View(self.request).render( 'settings.html', { 'form': UserSettingsForm( initial_data )} ))
		
	def post(self):

		form = UserSettingsForm( self.request )		
		if form.is_valid():		
			# get the values from the request and save them to the database
			Config.setKey('twitter_user', form.clean_data['twitter_user'])
			Config.setKey('delicious_user', form.clean_data['delicious_user'])
			Config.setKey('delicious_password', form.clean_data['delicious_password'])
			Config.setKey('youtube_user', form.clean_data['youtube_user'])		
			Config.setKey('google_reader_feed', form.clean_data['google_reader_feed'])					
		
			initial_data = {
				'twitter_user': Config.getKey( 'twitter_user' ),
				'delicious_user': Config.getKey( 'delicious_user' ),
				'delicious_password': Config.getKey( 'delicious_password' ),
				'youtube_user': Config.getKey( 'youtube_user' ),
				'google_reader_feed': Config.getKey( 'google_reader_feed' )
			}
		
			self.response.out.write( View(self.request).render( 'settings.html', { 
				'form': UserSettingsForm( initial_data ), 
				'message': 'Settings saved successfully'
			} ))
		else:
			# form not valid, must show again with the errors
			self.response.out.write( View(self.request).render( 'settings.html', { 
				'form': form,
				'message': 'There were some errors'
			} ))

class AdminMaintenance(webapp.RequestHandler):
	def get(self):
		self.response.out.write( View(self.request).render( 'admin_maintenance.html' ))

class DoAdminMaintenance(webapp.RequestHandler):
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

		self.response.out.write( View(self.request).render( 'admin_maintenance.html', { 'message': message } ))

def main():
  logging.getLogger().setLevel(logging.DEBUG)		
	
  application = webapp.WSGIApplication([('/admin/settings', UserSettings), ('/admin/maintenance', AdminMaintenance), ('/admin/maintenance/(.*)', DoAdminMaintenance)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()