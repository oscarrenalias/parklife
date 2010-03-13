from app.utils import templatehelpers

class BaseView:
	def render(self, template, view_values = []):
		raise Exception( 'BaseView.render is an abstract method!' )

class HTMLView(BaseView):	
	def render(self, template, view_values = []):		
		from google.appengine.ext.webapp import template as t
		import os		
		path = os.path.join(os.path.dirname(__file__), '../templates/' + template)
		return t.render(path, view_values)
		
class JSONView(BaseView):
	def render(self, template, view_values = []):
		from app.json import JSONHelper
		
		# we need to figure out when the stream was updated last
		return( JSONHelper().encode(view_values))
		
class AtomView(BaseView):
	def render(self, template, view_values = []):
		from google.appengine.ext.webapp import template as t
		from app.models.entry import Entry
		import os
		
		import app.utils.templatehelpers
		
		data=Entry().gql("ORDER BY created DESC").fetch(1)
		view_values['site']['last_updated'] = data[0].created		
		
		path = os.path.join(os.path.dirname(__file__), '../templates/atom.xml')
		return t.render(path, view_values)
		
class View:
	
	# list of renderers
	renderers = {}
	
	def __init__(self, request = None):
		self.__request = request
		
		# set up the list of available view renderers
		self.renderers = {
		   'html': HTMLView,
		   'json': JSONView,
		   'atom': AtomView
		}
	
	def render(self, template, view_values = {}, **params):
		if 'force_renderer' in params:
			output = params['force_renderer']
		else:
			if self.__request == None or self.__request.get('f') == '':
				output = 'html'
			else:
				output = self.__request.get('f')
			
		# is the renderer valid?
		if output not in self.renderers:
			raise Exception( 'Format not valid' )
			
		# merge some of the configuration data into the view data, in case it's needed
		from defaults import Defaults
		view_values['site'] = Defaults.site
		view_values['google_api_key'] = Defaults.GOOGLE_API_KEY
		# reference to the currently logged in user, if any
		from google.appengine.api import users
		view_values['user'] = users.get_current_user();
		view_values['user_is_admin'] = users.is_current_user_admin();
			
		# call the renderer
		return( self.renderers[output]().render(template, view_values ))