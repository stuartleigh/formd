import calendar
import datetime

from django.db import models
from django.utils import timezone


class AbstractPlan(models.Model):

	name = models.CharField(max_length=50, default="Default Plan")
	key = models.CharField(max_length=75)
	rate = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
	message_limit = models.IntegerField(default=0)

	class Meta:
		abstract = True


class Plan(AbstractPlan):
	selectable = models.BooleanField(default=False)

	def __str__(self):
		return "{name} ({key})".format(name=self.name, key=self.key)


class UserPlan(AbstractPlan):
	user = models.OneToOneField('account.User', related_name="plan")
	modified_time = models.DateTimeField()

	def start_of_cycle(self):
		from_date = date = self.user.date_joined
		now = timezone.now()

		while True:
			date += datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1])
			if date >= now:
				break
			from_date = date

		return from_date

	def save(self, *args, **kwargs):
		self.modified_time = timezone.now()
		return super(UserPlan, self).save(*args, **kwargs)
