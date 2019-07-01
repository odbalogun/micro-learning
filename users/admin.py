from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Student
from courses.models import Enrolled
from courses.admin import EnrolledInline
from olade.utilities import random_string


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'created_at')
    list_filter = ('is_superuser', 'created_at', 'is_active')
    exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions', 'last_login')

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.is_superuser = False
        obj.set_password(random_string(8))
        obj.created_by = request.user
        obj.save()

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
        obj.is_staff = False
        obj.is_superuser = False
        obj.set_password(random_string(8))
        obj.created_by = request.user
        obj.save()

    def get_queryset(self, request):
        return self.model.objects.filter(is_staff=False)


from constance.admin import ConstanceAdmin, Config
admin.site.unregister([Config])


# admin.site.register([Config], ConstanceAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.unregister(Group)