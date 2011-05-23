from app.models.entry import Entry
import logging

#
# base class for sources
#
class Source:
	
	source_id = ''
	
	#
	# Retrieves only the latest entries based on the timestamp of the last entry in the database
	# This method is to be implemented by child classes, otherwise it will throw a NotImplementedError exception
	#
	def getLatest(self):
		# get latest entries only
		raise NotImplementedError( 'Source.getLatest() must be implemented by child classes' )
				
	def persistEntry(self, e):
		e.put()
	
	#
	# converts whatever was read from the source system into an Entry object to be persisted
	# This method is to be implemented by child classes, otherwise it will throw a NotImplementedError exception
	# 
	def toEntry(self, item):
		raise NotImplementedError("Method toEntry() must be implemented by child classes")
		
	#
	# Returns true if an entry with the same twitter id already exists
	#
	def isDuplicate( self, entry ):
		if self.source_id == '':
			raise AssertionError("Source.source_id cannot be empty before using the Source.isDuplicate method")
		
		query = Entry.gql( 'WHERE external_id = :id AND source = :source', id = str(entry.external_id), source = self.source_id )
		value = False;
		if query.count() > 0: 
			value = True

		logging.debug( 'duplicate check: source = ' + self.source_id + ', id = ' + str(entry.external_id) + ', result = ' + str(value))
		return value
	
	#
	# returns the newest Entry object if the database, or None if none are found
	#
	def getMostRecentEntry(self):
		query = Entry.gql( 'WHERE source = :source ORDER BY created DESC', source=self.source_id)
		if query.count() == 0:
			return None
			
		return(query.fetch(1)[0])			
	
	#
	# processes the data retrieved by the source
	#
	def update(self):
		# persist each one of the entries after ensuring that they're not duplicates
		return(len(map(self.persistEntry, filter(lambda entry: self.isDuplicate(entry) == False, map(self.toEntry, self.getLatest())))))		