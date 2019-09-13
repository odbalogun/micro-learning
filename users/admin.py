from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from .models import User, Student
from .forms import AdminUserForm
from courses.models import Enrolled
from courses.admin import EnrolledInline
from olade.utilities import random_string
from django.contrib.sites.shortcuts import get_current_site


class UserAdmin(admin.ModelAdmin):
    form = AdminUserForm
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'created_at')
    fields = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_superuser', 'created_at', 'is_active')
    exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions', 'last_login')

    def save_model(self, request, obj, form, change):
        token = random_string(8)

        obj.is_staff = True
        obj.is_superuser = False
        obj.set_password(token)
        obj.created_by = request.user
        obj.save()

        current_site = get_current_site(request)
        domain = current_site.domain
        obj.email_user(subject="Your account has been created", title="Your account has been created",
                       subtitle="Your account has been created",
                       content="Your Olade account has been created. Your password is {}. To login, please click on "
                               "the button below".format(token), button_value="Log in", button_link="http://{}{}".
                       format(domain, reverse_lazy("users:login")))

    def get_queryset(self, request):
        return self.model.objects.filter(is_staff=True)


class StudentAdmin(admin.ModelAdmin):
    inlines = [
        EnrolledInline,
    ]
    list_display = ('first_name', 'last_name', 'email', 'enrolled_courses_count', 'is_active', 'created_at')
    fields = ('email', 'first_name', 'last_name', 'is_active')
    exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions', 'last_login')

    def save_model(self, request, obj, form, change):
        token = random_string(8)

        obj.is_staff = False
        obj.is_superuser = False
        obj.set_password(token)
        obj.created_by = request.user
        obj.save()

        obj.email_user(subject="Your account has been created", title="Your account has been created", 
                    subtitle="Your account has been created", 
                    content="Your Olade account has been created. Your password is {}".format(token))

    def get_queryset(self, request):
        return self.model.objects.filter(is_staff=False)


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.unregister(Group)