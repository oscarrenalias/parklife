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
		