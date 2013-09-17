from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class UserCreationForm(forms.ModelForm):
	error_messages = {
		'already_registered': 'That email address is already registered.',
	}

	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	password_repeat = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")

	class Meta:
		model = User
		fields = ('email',)

	def clean_email(self):
		email = self.cleaned_data['email']

		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email

		raise forms.ValidationError(self.error_messages['already_registered'])

	def clean_password_repeat(self):
		password = self.cleaned_data.get("password")
		password_repeat = self.cleaned_data.get("password_repeat")

		if password and password_repeat and password != password_repeat:
			raise forms.ValidationError(self.error_messages['password_mismatch'])

		return password_repeat

	def save(self, *args, **kwargs):
		user = super(UserCreationForm, self).save(commit=False)

		user.set_password(self.cleaned_data['password'])
		user.save()

		return authenticate(username=user.email, password=self.cleaned_data['password'])


class UserAuthenticationForm(AuthenticationForm):
	error_messages = {
		'invalid_login': "Your email address or password was invalid.",
        'inactive': "Your account is inactive.",
    }