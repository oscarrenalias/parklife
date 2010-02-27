from google.appengine.ext import db
import datetime

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
	
	# whether the object shouldn't be displayed
	deleted = db.BooleanProperty(default=False)
	
	def _make_slug(self, append=""):
		# It is possible to change the format of the slugs by modifying this
		# method.
		import re
		alphaspaces = re.compile(r"[^\w\s]")
		spaces = re.compile(r"\s")
		slug = spaces.sub("-", alphaspaces.sub(r"", self.title.lower()))
		slug = (slug + append).rstrip('-')

		return slug + append

	def _add_slug(self, slug_value):
		"Add a slug to the given datastore entity."

		query = self.gql ("WHERE slug = :slug", slug = slug_value )
		existing_slug = (query.count() > 0)

		if existing_slug:
			raise Exception

		return slug_value

	def set_slug(self):

		slug_try = self._make_slug()
		slug_iter = 0
		slug_good = False
		
		while not slug_good and slug_iter <= 10:
			# There will only be ten attempts to make the slug unique by
			# appending digits to it.  More than that probably indicates that
			# field specified in the call to slug_field_is does not have enough
			# differentiation.
			try:
				slug = self._add_slug(self._make_slug("_" + str(slug_iter) if slug_iter > 0 else ""))
				self.slug = slug
				slug_good = True
			except Exception:
				slug_iter += 1
			
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
	def permalink(self):
		from defaults import Defaults
		return( Defaults.site['base_url'] + '/entry/' + self.slug )
				
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