from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from .forms import UserCreationForm, UserAuthenticationForm
from concept.models import Concept


def sign_up(request):
	form = UserCreationForm(request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('my-account')

	context = {
		'form': form,
	}

	return TemplateResponse(request, 'account/sign_up.html', context)

def log_in(request):
	form = UserAuthenticationForm(data=request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('my-account')

	context = {
		'form': form,
	}

	return TemplateResponse(request, 'account/log_in.html', context)

def log_out(request):
	logout(request)
	return redirect('homepage')

@login_required
def my_account(request):
	return TemplateResponse(request, 'account/my_account.html', {})

@login_required
def my_plan(request):
	return TemplateResponse(request, 'account/my_plan.html', {})

@login_required
def my_password(request):
	form = PasswordChangeForm(request.user, data=request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			form.save()
			messages.success(request, 'Password changed successfully.')
			return redirect('my-account')

	context = {
		"form": form,
	}

	return TemplateResponse(request, 'account/my_password.html', context)
