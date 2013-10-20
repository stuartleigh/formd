import json
from urlparse import urlparse

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from formd.decorators import plan_required

from .forms import ConceptRequestValidationForm, ConceptEditForm, ConceptNewForm
from .models import Message, Concept


def get_concept_with_user(code, user):
	try:
		concept = Concept.objects.get(code=code)
	except Concept.DoesNotExist:
		raise http.Http404

	if user.has_perm('auth.change_concept'):
		return concept

	if user == concept.user:
		return concept

	raise http.Http404


def get_message_with_user(id, user):
	try:
		message = Message.objects.get(pk=id)
	except Message.DoesNotExist:
		raise http.Http404

	if user.has_perm('auth.change_message'):
		return message

	if user == message.concept.user:
		return message

	raise http.Http404


@csrf_exempt
def message_api(request):
	# get concept from request.POST
	origin = request.META.get('HTTP_ORIGIN')
	url = urlparse(origin)

	form = ConceptRequestValidationForm(request.POST, host=url.netloc)
	if not form.is_valid():
		return http.HttpResponseBadRequest("Error processing request: {}".format(form.errors))

	con = form.get_concept()

	msg = Message(
		concept=con,
		data=json.loads(json.dumps(request.POST))
	).save()

	if request.is_ajax():
		return http.HttpResponse(status=202)

	return_url = con.redirect_url or reverse('message-received')

	return http.HttpResponseRedirect(return_url)


def message_received(request):
	return http.HttpResponse("Message received, thank you")

@login_required
def my_concepts(request):

	concepts = Concept.objects.filter(user=request.user)

	context = {
		"concepts": concepts,
	}

	return TemplateResponse(request, 'concept/my_concepts.html', context)


@login_required
def view_concept(request, concept_code=None):

	concept = get_concept_with_user(concept_code, request.user)
	form = ConceptEditForm(request.POST or None, instance=concept)

	if request.method == "POST":
		if form.is_valid():
			form.save()
			messages.success(request, 'Form {} changed successfully.'.format(concept))
			return redirect('my-concepts')

	context = {
		"concept": concept,
		"form": form,
		"domain": settings.DOMAIN,
	}

	return TemplateResponse(request, 'concept/view_concept.html', context)

@login_required
def new_concept(request):
	form = ConceptNewForm(request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			concept = form.save(request.user)
			messages.success(request, 'Form {} added successfully.'.format(concept))
			return redirect('view-concept', concept_code=concept.code)

	context = {
		"form": form,
	}

	return TemplateResponse(request, 'concept/view_concept.html', context)

@login_required
def my_messages(request):

	messages = Message.objects.filter(concept__user=request.user)

	context = {
		"form_messages": messages,
	}
	return TemplateResponse(request, 'concept/my_messages.html', context)


@login_required
def view_message(request, message_id=None):

	message = get_message_with_user(message_id, request.user)

	context = {
		"message": message,
	}

	return TemplateResponse(request, 'concept/view_message.html', context)
