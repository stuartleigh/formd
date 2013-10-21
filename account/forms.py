from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMessage
import stripe

from .models import User, Domain


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
		user.send_welcome_email()
		user.set_default_plan()

		return authenticate(username=user.email, password=self.cleaned_data['password'])


class UserAuthenticationForm(AuthenticationForm):
	error_messages = {
		'invalid_login': "Your email address or password was invalid.",
        'inactive': "Your account is inactive.",
    }


class DomainForm(forms.ModelForm):

	class Meta:
		model = Domain
		fields = ('uri',)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(DomainForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		domain = super(DomainForm, self).save(commit=False)
		domain.user = self.user
		if commit:
			domain.save()

		return domain


class StripeTokenForm(forms.Form):
    stripeToken = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(StripeTokenForm, self).__init__(*args, **kwargs)

    def clean_stripeToken(self):
        stripe.api_key = settings.STRIPE_API_KEY
        try:
            self.customer = stripe.Customer.create(card=self.cleaned_data['stripeToken'], email=self.user.email)
        except stripe.CardError, error:
            err = error.json_body
            raise forms.ValidationError(err)

    def save(self):
        self.user.stripe_id = self.customer.id
        self.user.save()


class CloseAccountForm(forms.ModelForm):

    delete = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('is_active',)

    def clean_delete(self):
        val = self.cleaned_data['delete']
        if val.upper() != 'DELETE':
            raise forms.ValidationError('Invalid delete command')

    def save(self, *args, **kwargs):
        user = super(CloseAccountForm, self).save(commit=False)
        user.deactivate()

