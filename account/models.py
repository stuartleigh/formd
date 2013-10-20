from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.utils import timezone
import stripe

from plan.models import Plan, UserPlan, AbstractPlan
from concept.models import Message


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=CustomUserManager.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
        	email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)
    stripe_id = models.CharField(max_length=255, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def set_plan(self, plan):
    	if not isinstance(plan, Plan):
    		raise ValueError('plan must be of type Plan')

    	for field in AbstractPlan._meta.get_all_field_names():
    		setattr(self.plan, field, getattr(plan, field))

        if self.stripe_id and self.plan.rate:
            stripe.api_key = settings.STRIPE_API_KEY
            customer = stripe.Customer.retrieve(self.stripe_id)
            customer.update_subscription(plan=self.plan.key)

        self.plan.save()

    def set_default_plan(self):
        """ Only callable if userplan is not already set and if we have a pk """
        try:
            existing_plan = self.plan
            return
        except ObjectDoesNotExist:
            UserPlan(user=self).save()
            default_plan = Plan.objects.get(key="default")
            self.set_plan(default_plan)

    def send_welcome_email(self):
        msg = EmailMessage(
            to=[self.email],
            from_email=settings.FROM_EMAIL
        )
        msg.template_name = settings.WELCOME_EMAIL_TEMPLATE
        msg.template_content = {}
        msg.send()

    def valid_domains(self):
    	return [domain.uri for domain in self.domain_set.all()]

    def message_quota(self):
        limit = int(self.plan.message_limit)
        used = int(Message.objects.filter(concept__user=self, created_at__gte=self.plan.start_of_cycle()).count())

        perc = 100 if limit is 0 else float(used) / float(limit) * 100

        return {
            "limit": limit,
            "used": used,
            "perc": perc,
        }

    @property
    def available_message_count(self):
        quota = self.message_quota()
        return quota["limit"] - quota["used"]

    def deactivate(self):
        inactive_plan = Plan.objects.get(key="inactive")
        self.set_plan(inactive_plan)

        self.cancel_stripe_subscription()

        self.concept_set.update(active=False)

        self.is_active = False
        self.is_staff = False
        self.is_superuser = False

        self.save()

    def cancel_stripe_subscription(self):
        if not self.stripe_id:
            return

        stripe.api_key = settings.STRIPE_API_KEY
        cu = stripe.Customer.retrieve(self.stripe_id)
        cu.cancel_subscription()

class Domain(models.Model):

	user = models.ForeignKey(User)
	uri = models.CharField(max_length=100, db_index=True)


import account.signals
