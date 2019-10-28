from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings
from django.urls import reverse_lazy, reverse, re_path
from .models import User, Student
from .forms import AdminUserForm
from courses.admin import EnrolledInline
from olade.utilities import random_string
from django.contrib.sites.shortcuts import get_current_site
from super_inlines.admin import SuperModelAdmin
from django.utils.html import format_html
from mimetypes import guess_type
from django.http import HttpResponseRedirect, HttpResponse
from payments.models import PaymentLog
import os


class UserAdmin(admin.ModelAdmin):
    form = AdminUserForm
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'created_at')
    fields = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_superuser', 'created_at', 'is_active')
    exclude = ('is_staff', 'groups', 'user_permissions', 'last_login')

    def save_model(self, request, obj, form, change):
        token = random_string(8)

        obj.is_staff = True
        obj.is_superuser = True
        obj.set_password(token)
        obj.created_by = request.user
        obj.save()

        current_site = get_current_site(request)
        domain = current_site.domain
        obj.email_user(subject="Your account has been created", title="Your account has been created",
                       subtitle="Your account has been created",
                       content="Your Olade account has been created. Your password is {}. To login, please click on "
                               "the button below".format(token), button_value="Log in", button_link="http://{}{}".
                       format(domain, reverse_lazy("admin:index")))

    def get_queryset(self, request):
        return self.model.objects.filter(is_staff=True)


class StudentAdmin(SuperModelAdmin):
    class Media:
        js = ("update_course_fee.js", )

    inlines = (EnrolledInline, )
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'enrolled_courses_count',
                    'is_active', 'created_at', 'student_actions')
    fields = ('email', 'first_name', 'last_name', 'is_active')
    exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions', 'last_login')

    def save_model(self, request, obj, form, change):
        token = random_string(8)

        obj.is_staff = False
        obj.is_superuser = False
        obj.set_password(token)
        obj.created_by = request.user
        obj.save()

        current_site = get_current_site(request)
        domain = current_site.domain
        obj.email_user(subject="Your account has been created", title="Your account has been created",
                       subtitle="Your account has been created",
                       content="Your Olade account has been created. Your password is {}".format(token),
                       button_value="Log in", button_link="http://{}{}".format(domain, reverse_lazy("users:login")))

    def get_queryset(self, request):
        return self.model.objects.filter(is_staff=False)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, PaymentLog):
                instance.created_by = request.user
                if instance.enrolled.payment_status == 'partly':
                    amount = instance.enrolled.course.course_fee / 2
                    instance.amount_owed = amount
                else:
                    amount = instance.enrolled.course.course_fee
                instance.amount_paid = amount
            instance.save()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<student_id>.+)/download-identification/$',
                self.admin_site.admin_view(self.download_identification),
                name='download-identification',
            ),
        ]
        return custom_urls + urls

    def get_available_actions(self, obj):
        links = ''

        if obj.identity:
            links += '<a title="Download identification" href="{}"><i class="fa fa-download"></i></a> '.\
                format(reverse('admin:download-identification', args=[obj.pk]))
        return links

    def student_actions(self, obj):
        return format_html(self.get_available_actions(obj))

    def download_identification(self, request, student_id, *args, **kwargs):
        student = self.get_object(request, student_id)

        if not student:
            self.message_user(request, "Student entry could not be found", level='error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin:users_student_changelist')))

        if not student.identity:
            self.message_user(request, "Student has not provided identification", level='error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin:users_student_changelist')))

        file_path = student.identity.path
        if not os.path.exists(file_path):
            self.message_user(request, "Error! File not found. Advise student to re-upload", level='error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin:users_student_changelist')))

        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type=guess_type(file_path)[0])
            response['Content-Length'] = len(response.content)
            response['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(file_path))
            return response

    student_actions.short_description = 'actions'
    student_actions.allow_tags = True


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.unregister(Group)