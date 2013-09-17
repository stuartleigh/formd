from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from plan.models import UserPlan


@receiver(pre_save, sender=UserPlan)
def update_modified_time(sender, instance, **kwargs):
	instance.modified_time = timezone.now()