class forms:

	class BaseField:
		def __init__(self, required=True, label="", widget=0, name="", value=""):
			self.required = required
			self.label = label
			self.widget = widget
			self.name = name
			self.value = ""

		def render(self):
			return(self.widget.render(self))

	class CharField(BaseField):
		pass

	class widgets:

		class BaseWidget:
			def __init__(self, attrs):
				self.attrs = attrs

			def render(self, field):
				widget = '<p>'
				widget = '<label for="id_' + field.name +'">' + field.label + '</label><br/>'
				widget += self.childRender(field)
				widget += "</p>"

				return(widget)

			def childRender(self, field):
				return ""

		class TextInput(BaseWidget):
			type = "text"
			def childRender(self, field):
				widget = '<input type="' + self.type + '" name="id_' + field.name + '" '
				# process all field attributes, if any
				attributes = " ".join(map(lambda key: key + '="' + str(self.attrs[key]) + '" ', self.attrs.keys()))
				# set the value, if any
				if field.value != "":
					attributes += 'value ="' + field.value + '"'

				# close the form
				widget += attributes + ' />\n'

				return(widget)

		class PasswordInput(TextInput):
			type = "password"

	class Form:
		def __init__(self, values={}):
			self.values = values
			self.clean_data = {}
			for (k,v) in values.items():
				if self.__class__.__dict__.has_key(k):
					self.__class__.__dict__[k].value = v

				# save the cleaned up value, but only if it's one of the ones defined for the form
				if k[0:3] == "id_":
					k = k[3:]
				
				self.clean_data[k] = v

		def render(self):
			# retrieve all fields
			form = ""

			#for (field, fieldObj) in vars(self).items():
			for attr in self.__class__.__dict__.keys():
				fieldObj = getattr(self, attr)
				if isinstance(fieldObj, forms.BaseField):
					fieldObj.name = attr
					form += fieldObj.render()

			return(form)

		def is_valid(self):
			return(True)	# TODO: this will do for now!