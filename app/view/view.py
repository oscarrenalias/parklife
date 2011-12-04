from app.utils.templatehelpers import templatehelpers
from app.view.viewhelpers import ViewHelpers
import jinja2
from google.appengine.api import users
import os
import logging

class BaseView:

	jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates"))
	jinja.filters['slugify'] = templatehelpers.slugify
	jinja.filters['permalink'] = templatehelpers.permalink
	jinja.filters['atom_date'] = templatehelpers.atom_date
	jinja.filters['groupby_new'] = templatehelpers.do_groupby_new
	
	is_iphone = False
	request = None

	# specialized view rendereds can use this to ovewrite the default content type
	content = "text/html; charset=utf-8"

	def render(self, template, view_values = []):
		raise Exception( 'BaseView.render is an abstract method!' )
	
	#
	# partial views only return a part of the page instead of one entire page. Partial views are useful
	# for Ajax page transitions.
	# Partial views are forced by providing "b" as a parameter in the request
	#	
	def isPartialView(self):
		return self.request.get("b")
	
	#
	# in case of partial views, the convetion is that the template is called template_partial.html
	#
	def getPartialTemplateName(self, template):
		fileParts = template.split(".")
		template = fileParts[0] + "_partial." + ".".join(fileParts[1:])
		return(template)

	def getLoginUrl(self):
		return users.create_login_url(self.request.url)
	
	def getLogoutUrl(self):
		return users.create_logout_url(self.request.url)		
	
class MobileHTMLView(BaseView):
	def render(self, template, view_values = []):
		
		view_values['login_url'] = self.getLoginUrl()
		view_values['logout_url'] = self.getLogoutUrl()		

		path = os.path.join(os.path.dirname(__file__), '../templates/iphone/' + template)		
		data = t.render(path, view_values)
		
		return( data )

class HTMLView(BaseView):
	def render(self, template, view_values = []):		
		view_values['login_url'] = self.getLoginUrl()
		view_values['logout_url'] = self.getLogoutUrl()		

		if self.isPartialView(): # partial view has been requested
			template = self.getPartialTemplateName(template)
			
		#path = os.path.join(os.path.dirname(__file__), '../templates/' + template)			
		#data = t.render(path, view_values)
		template = self.jinja.get_template(template)
		data = template.render(view_values)

		return( data )
		
class JSONView(BaseView):
	content = "application/json; charset=utf-8"

	def render(self, template, view_values = []):
		from app.json.helper import JSONHelper		
		del view_values['defaults']

		response = JSONHelper().encode(view_values)	

		# check if this is a JSONP request, we can do so by checking if the 'calllback'
		# parameter is present in the request and then we'll wrap it around the json response
		if self.request.get('callback'):
			response = self.request.get('callback') + "(" + response + ")"

		return( response )
		
class AtomView(BaseView):
	content = "application/atom+xml; charset=utf-8"

	def render(self, template, view_values = []):
		import app.utils.templatehelpers
		from app.models.entry import Entry
		
		data=Entry().gql("ORDER BY created DESC").fetch(1)
		view_values['site']['last_updated'] = data[0].created		
		
		#path = os.path.join(os.path.dirname(__file__), '../templates/atom.xml')
		#return t.render(path, view_values)
		template = self.jinja.get_template("atom.xml")
		
		return(template.render(view_values))
		
class View:
	
	# list of renderers
	renderers = {}
	
	def __init__(self, template, request = None):
		self.request = request
		self.template = template
		
		# set up the list of available view renderers
		self.renderers = {
		   'html': HTMLView,
		   'json': JSONView,
		   'atom': AtomView,
		   'mobile': MobileHTMLView
		}
	
	def render(self, view_values = {}, **params):
		if 'force_renderer' in params:
			output = params['force_renderer']
		else:
			if self.request == None or self.request.get('f') == '':
				output = 'html'
			elif self.is_iphone():
				output = 'mobile'
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
		# return the rendered content as well as the correct content type
		return( renderer.render(self.template, view_values ), renderer.content)
		
	def is_iphone(self):
		#return _IPHONE_UA.search(self.request.headers['user-agent']) is not None
		return ViewHelpers.is_iphone(self.request.headers['user-agent'])