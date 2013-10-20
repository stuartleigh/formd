from django import forms
from django.http import request

import re

from concept.models import Concept

host_validation_re = re.compile(r"^([a-z0-9.-]+|\[[a-f0-9]*:[a-f0-9:]+\])(:\d+)?$")

def split_domain_port(host):
    """
    Return a (domain, port) tuple from a given host.

    Returned domain is lower-cased. If the host is invalid, the domain will be
    empty.
    """
    host = host.lower()

    if not host_validation_re.match(host):
        return '', ''

    if host[-1] == ']':
        # It's an IPv6 address without a port.
        return host, ''
    bits = host.rsplit(':', 1)
    if len(bits) == 2:
        return tuple(bits)
    return bits[0], ''



class ConceptRequestValidationForm(forms.Form):

    token = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.host = kwargs.pop('host')
        super (ConceptRequestValidationForm, self).__init__(*args, **kwargs)

    def clean_token(self):
        token = self.cleaned_data['token']

        try:
            self.con = con = Concept.active_objects.get(code=token)
        except Concept.DoesNotExist:
            raise forms.ValidationError('invalid token')

        valid_domains = con.user.valid_domains()

        host, port = split_domain_port(self.host)

        valid = request.validate_host(host, valid_domains)

        if not valid:
            raise forms.ValidationError('invalid domain')

        return token

    def clean(self):
        cleaned_data = super(ConceptRequestValidationForm, self).clean()
        if hasattr(self, 'con'):
            conn = self.get_concept()

            if conn.user.available_message_count < 1:
                raise forms.ValidationError("Account exceeded message quota")

        return cleaned_data

    def get_concept(self):
        return self.con


class ConceptEditForm(forms.ModelForm):

    class Meta:
        model = Concept
        fields = ("name", "honeypot", "email", "subject", "template", "redirect_url", "active")

class ConceptNewForm(forms.ModelForm):

    class Meta:
        model = Concept
        fields = ("name", "honeypot", "email", "subject", "template", "redirect_url")

    def save(self, user, *args, **kwargs):
        concept = super(ConceptNewForm, self).save(commit=False)
        concept.user = user
        concept.active = True
        concept.save()
        return concept

