from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Student


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_admin', 'created_at')
    list_filter = ('is_admin', 'created_at', 'is_active')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

    def get_queryset(self, request):
        return self.model.objects.filter(is_staff=False)


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.unregister(Group)