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
		if page == 1: 
			prev_page = page
		else:
			prev_page = page - 1
			
		next_page = page + 1
		
		val = super(PagedQuery, self).fetch(items_per_page, (page-1) * items_per_page)		
		return prev_page, val, next_page