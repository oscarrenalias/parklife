from google.appengine.ext import db

class CalculatedProperty(db.Property):
	
	def __init__(self, calc_fn, **kwds):
		super(CalculatedProperty, self).__init__(**kwds)
		self.calc_fn = calc_fn
		
	def __get__(self, model_instance, model_class):
		if model_instance is None:
			return self
		return self.calc_fn(model_instance)