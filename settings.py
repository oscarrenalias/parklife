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

import logging
from app.view.view import View
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from app.models.config import Config
from app.source.twitter import TwitterSource

#
# updates the twitter source
#
class UserSettings( webapp.RequestHandler ):
	
	def get(self):	
		# show the form to update the user settings
		twitter_user = Config.getKey( 'twitter_user' )
		delicious_user = Config.getKey( 'delicious_user' )
		self.response.out.write(View.render( 'settings.html', { 'twitter_user': twitter_user, 'delicious_user': delicious_user }))
		
	def post(self):
		# get the values from the request and save them to the database
		Config.setKey('twitter_user', self.request.get('twitter_user'))
		Config.setKey('delicious_user', self.request.get('delicious_user'))		
		twitter_user = Config.getKey( 'twitter_user' )
		delicious_user = Config.getKey( 'delicious_user' )		
		
		self.response.out.write(View.render( 'settings.html', { 'twitter_user': twitter_user, 'delicious_user': delicious_user, 'message': 'Settings sucessfully updated' }))

def main():
  logging.getLogger().setLevel(logging.DEBUG)		
	
  application = webapp.WSGIApplication([('/settings', UserSettings)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()