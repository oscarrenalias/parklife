from google.appengine.ext.db import djangoforms
from django import newforms as forms

#
# We monkeypatch the forms.BaseForm class from Django to implement
# a nicer form rendere, based on as_p but adding <br/> after every field label
#
class Forms(forms.BaseForm):
	__metaclass__ = djangoforms.monkey_patch
	def render(self):
		return self._html_output(u'<p>%(label)s<br/> %(field)s%(help_text)s</p>', u'<p>%s</p>', '</p>', u' %s', True)
		