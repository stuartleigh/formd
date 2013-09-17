import re
import uuid
import datetime

from django.conf import settings
from django_rq import job
from django.core.mail import send_mail


VARIABLE_TAG_START = "{{"
VARIABLE_TAG_END = "}}"

tag_re = re.compile('({}.*?{})'.format(re.escape(VARIABLE_TAG_START), re.escape(VARIABLE_TAG_END)))

def gen_code():
	id = uuid.uuid4()
	return id.hex

def simple_render(template, context):
    """ Takes a very simple template and substitues {{ token }} from context """

    def parse_token(token, in_tag):
        if not in_tag:
            return token
        var = token[2:-2].strip()
        return context.get(var, '')

    result = []
    in_tag = False

    for token in tag_re.split(template):
        if token:
            result.append(parse_token(token, in_tag))
        in_tag = not in_tag

    return ''.join(result)

@job
def send_message(message):
    concept = message.concept
    email = concept.email
    template = concept.template
    subject = concept.subject
    context = message.data

    email_subject = simple_render(subject, context)
    email_body = simple_render(template, context)

    send_mail(email_subject, email_body, settings.FROM_EMAIL, [email])
    message.sent = True
    message.sent_at = datetime.datetime.now()
    message.save()

