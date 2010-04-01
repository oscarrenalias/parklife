#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under GNU General Public License version 3:
# http://www.gnu.org/licenses/gpl-3.0.txt
#

from google.appengine.ext import db
from google.appengine.ext.db import Query

class PagedQuery(Query):
	
	def fetch(self, page, items_per_page = 20 ):
		
		limit = page * items_per_page
		offset = items_per_page
		next_page = page + 1
		
		#print 'page = %s, limit = %s, items_per_page = %s, offset = %s' % (page, limit, items_per_page, offset)
		
		if page == 1: 
			prev_page = page - 1
		else:
			prev_page = page
		
		val = super(PagedQuery, self).fetch(limit, offset)		
		return prev_page, val, next_page