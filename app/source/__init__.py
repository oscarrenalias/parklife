from app.models.entry import Entry
import logging

#
# base class for sources
#
class Source:
	
	source_id = ''
	
	def getAll(self):
		# get all entries
		print( 'getAll ')
		
	def getLatest(self):
		# get latest entries only
		print( 'getLatest' )
		
	def getLastUpdateDate(self):
		print( 'getLastUpdateDate' )
		
	def getLastUpdateExternalId(self):
		print( 'getLastUpdateDate' )
		
	#
	# returns true if an entry with the same twitter id already exists
	#
	def isDuplicate( self, id, source ):
		query = Entry.gql( 'WHERE external_id = :id AND source = :source', id = str(id), source = source )
		value = False;
		if query.count() > 0: 
			value = True

		logging.debug( 'duplicate check: ' + str(id) + ' result: ' + str(value))
		return value		