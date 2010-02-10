import os
from google.appengine.ext.webapp import template as t

class View:
	
	def render(template, template_values = []):
		path = os.path.join(os.path.dirname(__file__), '../templates/' + template)
		return t.render(path, template_values)
		
	# the render() method can be static
	render = staticmethod(render)