from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone

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

    	self.plan.save()

    def valid_domains(self):
    	return [domain.uri for domain in self.domain_set.all()]

    def concept_quota(self):
        limit = self.plan.form_limit
        used = self.concept_set.filter(active=True).count()
        perc = (used / limit) * 100
        return {
            "limit": limit,
            "used": used,
            "perc": perc,
        }

    @property
    def available_concept_count(self):
        quota = self.concept_quota()
        return quota["limit"] - quota["used"]

    def message_quota(self):
        limit = int(self.plan.message_limit)
        used = int(Message.objects.filter(concept__user=self).count())
        perc = float(used) / float(limit) * 100
        return {
            "limit": limit,
            "used": used,
            "perc": perc,
        }

    @property
    def available_message_count(self):
        quota = self.message_quota()
        return quota["limit"] - quota["used"]

    def domain_quota(self):
        limit = int(self.plan.domain_limit)
        used = int(self.domain_set.count())
        perc = float(used) / float(limit) * 100
        return {
            "limit": limit,
            "used": used,
            "perc": perc,
        }

    @property
    def available_domain_count(self):
        quota = self.message_quota()
        return quota["limit"] - quota["used"]

class Domain(models.Model):

	user = models.ForeignKey(User)
	uri = models.CharField(max_length=100, db_index=True)





import account.signals