import json

from django.db import models
from jsonfield import JSONField
from django.utils import timezone

from concept.utils import gen_code, simple_render, send_message


class ActiveManager(models.Manager):
	def get_queryset(self):
		return super(ActiveManager, self).get_queryset().filter(active=True)

class Concept(models.Model):
	name = models.CharField(max_length=254, blank=True)
	code = models.CharField(max_length=254, unique=True, editable=False, default=gen_code)
	user = models.ForeignKey('account.User')

	email = models.EmailField(max_length=254, blank=True)
	subject = models.CharField(max_length=254, blank=True)
	template = models.TextField(blank=True)
	honeypot = models.BooleanField(default=False)

	redirect_url = models.URLField(max_length=254, blank=True)

	active = models.BooleanField(default=False)

	objects = models.Manager()
	active_objects = ActiveManager()

	def __unicode__(self):
		return "{} - {}".format(self.name or 'Blank', self.code)


class Message(models.Model):

	message_id = models.CharField(max_length=254, blank=True, editable=False)
	concept = models.ForeignKey(Concept, editable=False)
	data = JSONField(blank=True)
	created_at = models.DateTimeField(default=timezone.now, editable=False)
	sent = models.BooleanField(default=False, editable=False)
	sent_at = models.DateTimeField(blank=True, null=True, editable=False)

	def render(self):
		return simple_render(self.concept.template, self.data)

	def save(self):
		super(Message, self).save()
		if not self.sent:
			self.send()

	def send(self):
		send_message.delay(self)
