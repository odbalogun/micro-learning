from django.contrib import admin
from django.urls import re_path, reverse
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from .models import Courses, Modules
from .forms import ModuleForm


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_fee', 'students_count', 'modules_count', 'is_active', 'created_by',
                    'created_at', 'course_actions')
    readonly_fields = ('course_actions',)
    list_filter = ('created_by', 'created_at')
    exclude = ('slug', 'created_at', 'created_by', 'is_active')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

    def get_urls(self):
        """
        Override urls so we can add our own urls for our custom actions
        :return: list of available urls
        """
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<course_id>.+)/add-module/$',
                self.admin_site.admin_view(self.process_add_module),
                name='add-module',
            ),
        ]
        return custom_urls + urls

    def process_add_module(self, request, course_id, *args, **kwargs):
        return self.process_action_form(
            request=request,
            course_id=course_id,
            action_form=ModuleForm,
            action_title='Add Module',
        )

    def process_action_form(self, request, course_id, action_form, action_title):
        course = self.get_object(request, course_id)

        if request.method != 'POST':
            form = action_form(initial={'course': course_id, 'created_by': request.user.id,
                                        'order': course.get_max_module_position+1})
        else:
            form = action_form(request.POST, initial={'course': course_id, 'created_by': request.user.id,
                                                      'order': course.get_max_module_position+1})

            if form.is_valid():
                try:
                    form.save()
                except form.errors.Error as e:
                    pass
                else:
                    self.message_user(request, 'Module created successfully')
                    url = reverse(
                        'admin:courses_courses_changelist',
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['course'] = course
        context['title'] = action_title
        return TemplateResponse(
            request,
            'admin/courses/add_module.html',
            context,
        )

    def course_actions(self, obj):
        return format_html('<a class="button" href="{}">Add Module</a>&nbsp;',
                           reverse('admin:add-module', args=[obj.pk]))

    course_actions.short_description = 'Actions'
    course_actions.allow_tags = True


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'order', 'access_code', 'created_by', 'created_at')
    list_filter = ('created_by', 'created_at', 'course')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


admin.site.register(Courses, CourseAdmin)
admin.site.register(Modules, ModuleAdmin)