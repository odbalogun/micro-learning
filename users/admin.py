from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Student


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'created_at')
    list_filter = ('is_superuser', 'created_at', 'is_active')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'created_at')
    fields = ('email', 'first_name', 'last_name', 'password')
    exclude = ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'last_login')

    def save_model(self, request, obj, form, change):
        obj.is_staff = False
        obj.is_superuser = False
        obj.save()

    def get_queryset(self, request):
        return self.model.objects.filter(is_staff=False)


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.unregister(Group)