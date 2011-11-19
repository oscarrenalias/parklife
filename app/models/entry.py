from google.appengine.ext import db
from app.db import CalculatedProperty
import datetime
import logging

class Entry(db.Model):
	# creation date
	created = db.DateTimeProperty(auto_now_add=True)
	
	# external id - can be used to store the source's own identifier, e.g
	# twitter's own tweet id
	external_id = db.StringProperty()
	
	# source identifier/name
	source = db.StringProperty()
	
	# title of the entry
	title = db.StringProperty()
	
	# text of the entry
	text = db.TextProperty()
	
	# is there a link pointing to this url?
	url = db.LinkProperty()
	
	# tags, for those sources that support them
	tags = db.StringListProperty()
	
	# slug
	slug = db.StringProperty()
	
	# latitude
	lat = db.StringProperty()
	
	# longitude
	lng = db.StringProperty()
	
	# name of the location, if any
	location_name = db.StringProperty()
	
	# whether the object shouldn't be displayed
	deleted = db.BooleanProperty(default=False)
	
	# attribute specific to the twitter source
	twitter_reply = db.BooleanProperty(default=False)

	#
	# this is only used for grouping entries at the template level
	#
	def created_date(self):
		return self.created.strftime("%B %d, %Y")
	
	# for date handling
	@CalculatedProperty
	def month(self):
		return self.created.month
		
	@CalculatedProperty
	def year(self):
		return self.created.year
		
	@CalculatedProperty
	def day(self):
		return self.created.day

	def _make_slug(self, append=""):
		# It is possible to change the format of the slugs by modifying this
		# method.
		import re
		alphaspaces = re.compile(r"[^\w\s]")
		spaces = re.compile(r"\s")
		slug = spaces.sub("-", alphaspaces.sub(r"", self.title.lower()))
		slug = (slug + append).rstrip('-')

		return slug + append

	def _slug_exists(self, slug_value):
		if self.is_saved() == False:
			query = self.gql ("WHERE slug = :slug", slug = slug_value )
			existing_slug = (query.count() > 0)
		else:
			query = self.gql ("WHERE slug = :slug", slug = slug_value)
			if query.count() == 1:
				# is it ourselves?
				entry = query.fetch(1)
				if entry[0].key() == self.key():
					existing_slug = False
				else:
					existing_slug = True
			else:
				existing_slug = False

		return existing_slug	

	def set_slug(self):

		slug_try = self._make_slug()
		slug_iter = 0
		slug_good = False
		
		while not slug_good and slug_iter <= 10:
			# There will only be ten attempts to make the slug unique by
			# appending digits to it.  More than that probably indicates that
			# field specified in the call to slug_field_is does not have enough
			# differentiation.
			
			slug = self._make_slug("_" + str(slug_iter) if slug_iter > 0 else "")
			if self._slug_exists(slug):
				slug_iter += 1
			else:
				self.slug = slug
				slug_good = True				
			
		if slug_iter == 11:
			# We have exceeded the maximum number of allowable attempts to de-dupe the slug, so throw
			# an exception.
			raise Exception, "Could not create a unique slug value."			
			
	def put(self):
		self.set_slug()
		#self.tag_list = self.getTasList()
		return(super(Entry, self).put())
		
	#
	# returns a permanent link to the entry
	#	
	def permalink(self, f=None):
		from defaults import Defaults
		if f:
			f = "?f=" + f
		else:
			f = ""
		return( Defaults.site['base_url'] + '/entry/' + self.slug + f )

	#
	# link to this entry in admin interface, via REST
	#
	def service_link(self):
		from defaults import Defaults
		return( Defaults.site['base_url'] + '/service/entry/' + str(self.key()))
				
	#
	# for this specific model, the value of tag_list is calculated dynamically
	# so we need to ensure that its value is calcualted when the model is loaded
	# and mapped from its db entity
	#
  	#@classmethod	
	#def from_entity(cls, entity):
	#	val = super(Entry, cls).from_entity(entity)
	#	if val.tags != None: 
	#		val.tag_list = val.tags.split()
	#	else: 
	#		val.tag_list = []
	#	return val
	
	def __json__(self):
		properties = self.properties().items() 
		output = {} 
		for field, value in properties: 
			output[field] = getattr(self, field) 
		
		# this is not a real attribute of the object but we want to have it in the serialized json output
		output['permalink'] = self.permalink()
		output['service_link'] = self.service_link()
		output['permalink_json'] = self.permalink('json')
		output['permalink_atom'] = self.permalink('atom')
		
		return output
	
	#
	# Returns a bunch of entries based on the commonly used filters used for the public portion of the
	# site. Returns a Query object that can be used to iterate through the results
	#
	@staticmethod
	def getPagedQueryWithBasicFilters(extraFilters = {}):
		from defaults import Defaults
		from app.pager.pagedquery import PagedQuery		
		query = PagedQuery(Entry).filter('deleted = ', False).order( '-created' )
		
		for key in extraFilters:
			query.filter(key, extraFilters[key]) 
		
		if Defaults.TWITTER_IGNORE_AT_REPLIES:
			query = query.filter('twitter_reply = ', False )
			
		return query