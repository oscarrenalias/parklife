import unittest
from webapp2 import Request
from app.forms.forms import forms

class TestForms(unittest.TestCase):

	# sample form
	class UserSettingsForm(forms.Form):
		delicious_password = forms.CharField(required=False, label='Delicious password', seq=3, widget=forms.widgets.PasswordInput(attrs={'size':60}))
		twitter_user = forms.CharField(required=False, label='Twitter user', seq=1, widget=forms.widgets.TextInput(attrs={'size':60, 'class':'test-class', 'id':'test-id'}))
		delicious_user = forms.CharField(required=False, label='Delicious user', seq=2,widget=forms.widgets.TextInput(attrs={'size':60}))

	class EntryForm(forms.Form):
		title = forms.CharField(label='Title for the blog post', widget=forms.widgets.TextInput(attrs={'size':60, 'class': 'full-width'}))
		text = forms.CharField(label='Text for the blog post', widget=forms.widgets.TextArea(attrs={'rows': 14, 'cols': 60, 'class': 'mceEditor full-width' }))
		tags = forms.CharField(required=False,label='Tags', widget=forms.widgets.TextInput(attrs={'size':60, 'class': 'full-width'}))
		lat = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={'size':15}))
		lng = forms.CharField(required=False, widget=forms.widgets.HiddenInput(attrs={'size':15}))		

	def testEmptyForm(self):
		print("Empty form:\n" + self.UserSettingsForm().render() + "\n")

		# let's use visual validation for now...
		self.assertTrue(True)

	def testFormWithData(self):
		form = self.UserSettingsForm({
			'twitter_user': 'twitter_user_value',
			'delicious_user': 'delicious_user_value',
			'delicious_password': 'delicious_password_value'
		})

		formContents = form.render()
		print("Form with initial data:\n" + formContents + "\n")

		self.assertTrue(form.clean_data['twitter_user'], 'twitter_user_value')

	def testFormWithPOSTData(self):
		request = Request.blank('/')
		request.method = 'POST'
		request.body = 'id_twitter_user=twitter_user_value&id_delicious_value=delicious_user_value&id_delicious_password=delicious_password_value'

		form = self.UserSettingsForm(request.POST)

		formContents = form.render()
		print("Form with POST data:\n" + formContents + "\n")

		self.assertTrue(form.clean_data['twitter_user'], 'twitter_user_value')

	def testEntryForm(self):
		form = self.EntryForm()
		print("Entry form: " + form.render())
		self.assertTrue(True)