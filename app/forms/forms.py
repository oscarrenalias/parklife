#
# Reimplementation of Django's newforms
#
import logging

class forms:

	field_prefix = "id_"

	class BaseField:
		errors = []
		is_valid = True
		
		def __init__(self, required=True, label="", seq=999, widget=None, name="", value="", default_error = "This field is required."):
			self.required = required
			self.label = label
			self.widget = widget
			self.name = name
			self.value = value
			self.seq = seq
			self.error = default_error

		def render(self):
			return(self.widget.render(self))

		def clean(self, value):
			# child classes should provide a better implementation
			return value.strip()

		def set_value(self, value):
			self.value = value
			self.clean_value = self.clean(value)

		def is_valid(self):
			#print("is_valid = " + self.name + ", required = " + str(self.required) + ", value = " + self.value)
			# child classes could provide a better implementation
			if self.required == True and self.value == "":
				self.errors = [ self.error ]
				raise ValueError(self.error)

			return True

		def __repr__(self):
			return "<Field: type=%s, %s>" % (self.__class__.__name__, ", ".join(map(lambda x: str(x[0]) + ": " + str(x[1]), self.__dict__.iteritems())))

	class CharField(BaseField):
		pass

	class widgets:

		class BaseWidget:
			def __init__(self, attrs):
				self.attrs = attrs

			def render(self, field):
				widget = '<p>'
				widget += '<label for="' + self.addPrefix(field.name) +'">' + field.label + '</label><br/>'
				widget += self.childRender(field)
				widget += "</p>\n"

				return(widget)

			def joinAttributes(self, field):
				self.attrs['name'] = self.addPrefix(field.name)
				if self.attrs.has_key('id') == False:
					self.attrs['id'] = self.addPrefix(field.name)

				return " ".join(map(lambda key: key + '="' + str(self.attrs[key]) + '" ', self.attrs.keys()))

			def childRender(self, field):
				return ""
			
			def addPrefix(self, name):
				return forms.field_prefix + name

			def __repr__(self):
				return "<Widget: type = %s, %s>" % (self.__class__.__name__, str(self.attrs))

		class TextInput(BaseWidget):
			type = "text"
			def childRender(self, field):
				widget = '<input type="' + self.type + '" '
				# process all field attributes, if any
				attributes = self.joinAttributes(field)
				# set the value, if any
				if field.value != "":
					attributes += 'value ="' + field.value + '"'

				# close the form
				widget += attributes + ' />'

				return(widget)

		class PasswordInput(TextInput):
			type = "password"

		class TextArea(BaseWidget):
			def childRender(self, field):
				widget = '<textarea name="' + self.addPrefix(field.name) + '" '
				widget += self.joinAttributes(field) + ' />' + field.value + '</textarea>'
				return(widget)

		class HiddenInput(TextInput):
			type ="hidden"
			def render(self, field):
				widget = '<input type="' + self.type + '" '
				attributes = self.joinAttributes(field)
				# set the value, if any
				if field.value != "":
					attributes += 'value ="' + field.value + '"'
				# close the form
				widget += attributes + ' />\n'

				return(widget)				


	class Form:

		is_bound = False
		fields = {}
		data = {}
		clean_data = {}

		def __init__(self, values={}):

			# set the form fields
			self.fields = self._setFields()

			# is the form bound to any data?
			if len(values) > 0:
				is_bound = True

			for (k,v) in values.items():
				if self.__class__.__dict__.has_key(k):
					self.__class__.__dict__[k].value = v

				# save the cleaned up value, but only if it's one of the ones defined for the form
				if k[0:3] == forms.field_prefix:
					k = k[3:]
				
				self.data[k] = v
				self.clean_data[k] = self.fields[k].clean(v)
				self.fields[k].set_value(v)

			logging.debug(self)

		def __repr__(self):
			return "<Form: fields: %s, values: %s, clean_data: %s, is_bound: %s >" % (str(self.fields), str(self.data), str(self.clean_data), str(self.is_bound))
		
		# saves the fields in an internal list
		def _setFields(self):
			fields = {}
			for attr, obj in filter(lambda x: isinstance(x[1], forms.BaseField), self.__class__.__dict__.iteritems()):
				obj.name = attr
				fields[attr] = obj	
				
			return fields			

		def render(self):
			# retrieve all fields, filter out those that are not form fields and then sort them by their
			# sequence number field
			result = ""

			for field in sorted(self.fields.itervalues(), key=lambda f: f.seq):
				result += field.render()

			return(result)

		def __iter__(self):
			for name, field in self.fields.items():
				yield field			

		# determines if the values provided to the form are all valid
		def is_valid(self):
			valid = True
			for name, field in self.fields.iteritems():
				try:
					field.is_valid()
				except ValueError, msg:
					valid = False

			return valid