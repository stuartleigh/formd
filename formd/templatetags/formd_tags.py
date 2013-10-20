from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django import template

register = template.Library()

@register.tag()
def absolute_url(url_name):
    return "http://{ domain }{ path }".format(
        domain=settings.DOMAIN,
        path=reverse(url_name)
        )