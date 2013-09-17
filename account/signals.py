from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from account.models import User
from plan.models import UserPlan

@receiver(user_logged_in)
def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])


@receiver(post_save, sender=User)
def ensure_user_plan(sender, instance, created, **kwargs):
	try:
		plan = instance.plan
	except UserPlan.DoesNotExist:
		UserPlan(user=instance).save()