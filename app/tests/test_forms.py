import unittest
from webapp2 import Request
from app.view.forms import forms

class TestForms(unittest.TestCase):

	# sample form
	class UserSettingsForm(forms.Form):
		twitter_user = forms.CharField(required=False, label='Twitter user', widget=forms.widgets.TextInput(attrs={'size':60, 'class':'test-class', 'id':'test-id'}))
		delicious_user = forms.CharField(required=False, label='Delicious user', widget=forms.widgets.TextInput(attrs={'size':60}))
		delicious_password = forms.CharField(required=False, label='Delicious password', widget=forms.widgets.PasswordInput(attrs={'size':60}))

	def testEmptyForm(self):
		form = self.UserSettingsForm()
		formContents = form.render()

		print("Empty form:\n" + formContents + "\n")

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