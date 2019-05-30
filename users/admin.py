from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()



# Register your models here.
admin.site.register(User)
admin.site.unregister(Group)