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
				widget = '<input type="' + self.type + '"'
				if field.value:
					 widget += 'value="' + str(field.value) + '"'
				if self.attrs.has_key('size'):
					widget += ' size="' + str(self.attrs['size']) + '"'
				widget += ' />\n'

				return(widget)

		class PasswordInput(TextInput):
			type = "password"

	class Form:
		def __init__(self, values={}):
			self.values = values

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