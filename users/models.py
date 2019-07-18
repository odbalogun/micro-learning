from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from safedelete.models import SafeDeleteModel
from django.core.mail import send_mail
from .managers import UserManager
from constance import config as custom_config


class User(SafeDeleteModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def enrolled_courses_count(self):
        return self.enrolled_courses.count()

    def to_json(self):
        return {
            "id": self.pk,
            "email": self.email,
            "full_name": self.get_full_name(),
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def email_user(self, subject, message, from_email=custom_config.APP_EMAIL_ADDRESS, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], auth_user=custom_config.APP_EMAIL_ADDRESS,
                  auth_password=custom_config.APP_EMAIL_PASSWORD, **kwargs)

    enrolled_courses_count.short_description = 'Courses count'


class Student(User):
    """
    Proxy model so we can separate logic for students from that for admin users in Django admin
    """
    class Meta:
        proxy = True


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_user_receiver(sender, instance, created, **kwargs):
    """
    Send an email to users, created by admins, with their passwords
    """
    if created and instance.created_by:
        print("here II")
        instance.email_user("Your account has been created",
                            "Your Olade has been created. Your password is {}".format(instance._password))