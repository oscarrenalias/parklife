import unittest
from webapp2 import Request
from app.forms.forms import forms

class TestForms(unittest.TestCase):

	# sample forms
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
		# TODO: make sure that the rendered content is actually what we wanted
		self.assertNotEquals("", self.UserSettingsForm().render())

	def testFormWithData(self):
		form = self.UserSettingsForm({
			'twitter_user': 'twitter_user_value',
			'delicious_user': 'delicious_user_value',
			'delicious_password': 'delicious_password_value'
		})

		self.assertNotEquals("", form.render())
		self.assertTrue(form.clean_data['twitter_user'], 'twitter_user_value')
		self.assertTrue(form.clean_data['delicious_user'], 'delicious_user_value')
		self.assertTrue(form.clean_data['delicious_password'], 'delicious_password_value')

	def testFormWithPOSTData(self):
		request = Request.blank('/')
		request.method = 'POST'
		request.body = 'id_twitter_user=twitter_user_value&id_delicious_user=delicious_user_value&id_delicious_password=delicious_password_value'

		form = self.UserSettingsForm(request.POST)

		formContents = form.render()
		self.assertTrue(form.clean_data['twitter_user'], 'twitter_user_value')
		self.assertTrue(form.clean_data['delicious_user'], 'delicious_user_value')

	def testEntryForm(self):
		form = self.EntryForm()
		self.assertNotEquals("", form.render())

	def testEntryFormWithData(self):
		request = Request.blank('/')
		request.method = 'POST'
		request.body = 'id_title=title&id_text=text&id_tags=tags'

		form = self.EntryForm(request.POST)
		#self.assertTrue(form.is_valid())
		self.assertNotEquals("", form.render())
		self.assertEquals(form.clean_data['title'], 'title')
		self.assertEquals(form.clean_data['text'], 'text')
		self.assertEquals(form.clean_data['tags'], 'tags')

	def testInvalidForm(self):
		request = Request.blank('/')
		request.method = 'POST'
		request.body = 'id_title=&id_text=a&id_tags='

		form = self.EntryForm(request.POST)
		
		# vaidation should fail
		self.assertFalse(form.is_valid())	

		# and make sure that there's errors for fields where there should be errors
		self.assertEquals(1, len(form.title.errors))
		self.assertEquals(0, len(form.text.errors))
		# and that there's no error for the 'tags' field
		self.assertEquals(0, len(form.tags.errors))

	def testFormWithEntity(self):
		# create a test entity
		class TestEntity:
			pass

		e = TestEntity()
		e.title = "this is the title"
		e.text = "this is the text"
		e.tags = "tag1 tag2 tag3".split(' ')
		e.lat = "123"
		e.lng = "123"
		e.source = 'blog'
				
		# now use it to pre-fill the form
		form = self.EntryForm(instance=e)

		print(form.render())

		self.assertNotEquals("", form.render())