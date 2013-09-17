from django import http
from django.template.response import TemplateResponse


def homepage(request):
	return TemplateResponse(request, 'homepage.html', {})

def getting_started(request):
    return TemplateResponse(request, 'getting_started.html', {})