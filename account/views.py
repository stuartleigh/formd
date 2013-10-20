from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse

from .forms import UserCreationForm, UserAuthenticationForm, DomainForm, CloseAccountForm
from .models import Domain
from concept.models import Concept, Message


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
def my_domains(request):
	domains = request.user.domain_set.all()
	form = DomainForm(request.POST or None, user=request.user)

	if request.method == "POST":
		if form.is_valid():
			domain = form.save()
			messages.success(request, "Domain {} added successfully".format(domain.uri))
			return redirect('my-domains')

	context = {
		"domains": domains,
		"form": form,
	}
	return TemplateResponse(request, 'account/my_domains.html', context)

@login_required
def delete_domain(request, id):
	domain = get_object_or_404(Domain, pk=id)

	if request.user != domain.user:
		raise http.Http404

	domain.delete()
	messages.success(request, "Domain {} deleted successfully".format(domain.uri))
	return redirect('my-domains')

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

@login_required
def close_account(request):
	form = CloseAccountForm(data=request.POST or None, instance=request.user)

	if request.method == "POST":
		if form.is_valid():
			form.save()
			logout(request)
			messages.success(request, 'Account closed successfully.')
			return redirect('homepage')

	context = {
		"form": form,
		"total_messages": Message.objects.filter(concept__user=request.user).count(),
	}

	return TemplateResponse(request, 'account/close_account.html', context)