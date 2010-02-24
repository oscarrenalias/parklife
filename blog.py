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
from django import newforms as forms

#
# form object for the new blog entry
#
class BlogPostForm(forms.Form):
	title = forms.CharField(label='Title for the blog post', widget=forms.widgets.TextInput(attrs={'size':80}))
	text = forms.CharField(label='Text for the blog post', widget=forms.widgets.Textarea(attrs={'rows': 14, 'cols': 80, 'class': 'mceEditor' }))
	tags = forms.CharField(required=False,label='Tags', widget=forms.widgets.TextInput(attrs={'size':80}))
	

class BlogHandler(webapp.RequestHandler):	

	def get(self):	
		# display the form
		self.response.out.write( View.render( 'new_blog_post.html', { 'form': BlogPostForm() } ))

	def post(self):
		form = BlogPostForm( self.request )
		if form.is_valid():
			# validation successful, we can save the data
			e = Entry()
			e.title = form.clean_data['title']
			e.text = form.clean_data['text']
			e.tags = form.clean_data['tags']
			e.source = 'blog'
			e.put()
			
			# redirect to the main page
			self.redirect( '/' )
		else:
			# form not valid, must show again with the errors
			self.response.out.write( View.render( 'new_blog_post.html', { 'form': form } ))

def main():
  logging.getLogger().setLevel(logging.DEBUG)	
	
  application = webapp.WSGIApplication([('/blog', BlogHandler)], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()