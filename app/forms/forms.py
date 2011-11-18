class forms:

	class BaseField:
		def __init__(self, required=True, label="", seq=999, widget=0, name="", value=""):
			self.required = required
			self.label = label
			self.widget = widget
			self.name = name
			self.value = ""
			self.seq = seq

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
				widget += '<label for="id_' + field.name +'">' + field.label + '</label><br/>'
				widget += self.childRender(field)
				widget += "</p>\n"

				return(widget)

			def joinAttributes(self):
				return " ".join(map(lambda key: key + '="' + str(self.attrs[key]) + '" ', self.attrs.keys()))

			def childRender(self, field):
				return ""

		class TextInput(BaseWidget):
			type = "text"
			def childRender(self, field):
				widget = '<input type="' + self.type + '" name="id_' + field.name + '" '
				# process all field attributes, if any
				attributes = self.joinAttributes()
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
				widget = '<textarea name="id_' + field.name + '" '
				widget += self.joinAttributes() + ' />' + field.value + '</textarea>'
				return(widget)

		class HiddenInput(TextInput):
			type ="hidden"
			def render(self, field):
				widget = '<input type="' + self.type + '" name="id_' + field.name + '" '
				attributes = self.joinAttributes()
				# set the value, if any
				if field.value != "":
					attributes += 'value ="' + field.value + '"'
				# close the form
				widget += attributes + ' />\n'

				return(widget)				


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
			# retrieve all fields, filter out those that are not form fields and then sort them by their
			# sequence number field
			result = ""
			for attr, obj in sorted(filter(lambda x: isinstance(x[1], forms.BaseField), self.__class__.__dict__.iteritems()), key=lambda x: x[1].seq):
				obj.name = attr
				result += obj.render()

			return(result)

		def is_valid(self):
			return(True)	# TODO: this will do for now!