from django.db import models
from django.conf import settings
from safedelete.models import SafeDeleteModel


class Courses(SafeDeleteModel):
    name = models.CharField('name', blank=False, max_length=50)
    description = models.TextField('description', blank=False)
    fees = models.FloatField('fees')
    is_active = models.BooleanField('is active', default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_courses', on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses')


class Modules(SafeDeleteModel):
    course = models.ForeignKey(Courses, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField('name', blank=False, max_length=50)
    description = models.TextField('description')
    access_url = models.CharField('access url', max_length=50)
    order = models.IntegerField('order')
    date_created = models.DateTimeField('date created', auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='modules', through="UserModules")

    class Meta:
        unique_together = ('course', 'order')


class UserModules(SafeDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_modules', on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, related_name='user_modules', on_delete=models.CASCADE)
    date_activated = models.DateTimeField('date activated', auto_now_add=True)
    expires = models.DateTimeField('date expires')

    class Meta:
        unique_together = ('user', 'module')