from django.db import models
from django.contrib.auth.models import AbstractUser
from safedelete.models import SafeDeleteModel

from .managers import UserManager


class User(SafeDeleteModel, AbstractUser):
    email = models.EmailField('email address', unique=True, blank=False)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_admin = models.BooleanField('is admin', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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

    def to_json(self):
        return {
            "id": self.pk,
            "email": self.email,
            "full_name": self.get_full_name(),
            "first_name": self.first_name,
            "last_name": self.last_name
        }
