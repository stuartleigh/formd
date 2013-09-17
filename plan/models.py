from django.db import models

from django.utils import timezone


class AbstractPlan(models.Model):

	name = models.CharField(max_length=50, default="Default Plan")
	rate = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
	domain_limit = models.IntegerField(default=0)
	form_limit = models.IntegerField(default=0)
	message_limit = models.IntegerField(default=0)

	class Meta:
		abstract = True


class Plan(AbstractPlan):
	selectable = models.BooleanField(default=False)


class UserPlan(AbstractPlan):
	user = models.OneToOneField('account.User', related_name="plan")
	modified_time = models.DateTimeField()

	def save(self, *args, **kwargs):
		self.modified_time = timezone.now()
		return super(UserPlan, self).save(*args, **kwargs)
