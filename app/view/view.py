from app.utils import templatehelpers
from app.view.viewhelpers import ViewHelpers

class BaseView:
	
	is_iphone = False
	request = None
	
	def render(self, template, view_values = []):
		raise Exception( 'BaseView.render is an abstract method!' )

class HTMLView(BaseView):	
	def render(self, template, view_values = []):		
		from google.appengine.ext.webapp import template as t
		from google.appengine.api import users
		import django.template 
		import os
		
		# create the login and logout urls in case they are needed in the template
		
		view_values['login_url'] = users.create_login_url(self.request.url);
		view_values['logout_url'] = users.create_logout_url(self.request.url)		

		# if the device is an iphone, try to load the iphone template for the given page
		if self.is_iphone:
			path = os.path.join(os.path.dirname(__file__), '../templates/iphone/' + template)
		else:
			path = os.path.join(os.path.dirname(__file__), '../templates/' + template)
			
		# if the iphone cannot be found then fallback on the normal HTML one
		try:
			data = t.render(path, view_values)
		except django.template.TemplateDoesNotExist:
			if self.is_iphone:
				# if we were trying to render the mobile view, try without...
				data = t.render(os.path.join(os.path.dirname(__file__), '../templates/' + template), view_values )
				
		return( data )
		
class JSONView(BaseView):
	def render(self, template, view_values = []):
		from app.json.helper import JSONHelper		
		del view_values['defaults']

		response = JSONHelper().encode(view_values)	

		# check if this is a jsonp request, we can do so by checking if the 'calllback'
		# parameter is present in the request and then we'll wrap it around the json response
		if self.request.get('callback'):
			response = self.request.get('callback') + "(" + response + ")"

		return( response )
		
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
		self.request = request
		
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
			if self.request == None or self.request.get('f') == '':
				output = 'html'
			else:
				output = self.request.get('f')
			
		# is the renderer valid?
		if output not in self.renderers:
			raise Exception( 'Format not valid' )
			
		# merge some of the configuration data into the view data, in case it's needed
		from defaults import Defaults
		view_values['defaults'] = Defaults
		view_values['site'] = Defaults.site
		# reference to the currently logged in user, if any
		from google.appengine.api import users
		view_values['user'] = users.get_current_user();
		view_values['user_is_admin'] = users.is_current_user_admin();
			
		# call the renderer
		renderer = self.renderers[output]()
		renderer.is_iphone = self.is_iphone()
		renderer.request = self.request
		return( renderer.render(template, view_values ))
		
	def is_iphone(self):
		#return _IPHONE_UA.search(self.request.headers['user-agent']) is not None
		return ViewHelpers.is_iphone(self.request.headers['user-agent'])