from django.contrib import admin
from django.urls import re_path, reverse, reverse_lazy
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.contrib.admin.views.main import ChangeList
from .models import Courses, Modules, Enrolled
from .forms import ModuleForm


class EnrolledInline(admin.StackedInline):
    model = Enrolled
    extra = 1
    can_delete = True


class EnrolledAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'current_module', 'status', 'payment_status', 'date_enrolled', 'enrolled_actions')
    search_fields = ['user__first_name', 'user__last_name', 'course__name']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<enrolled_id>.+)/promote-next-module/$',
                self.admin_site.admin_view(self.promote_next_module),
                name='promote-next-module',
            ),
            re_path(
                r'^(?P<enrolled_id>.+)/enrolled-modules/$',
                self.admin_site.admin_view(self.enrolled_modules),
                name='enrolled-modules',
            ),
        ]
        return custom_urls + urls

    def promote_next_module(self, request, enrolled_id, *args, **kwargs):
        enrolled = self.get_object(request, enrolled_id)
        if enrolled:
            # get next module
            try:
                module = Modules.objects.filter(course=enrolled.course, order__lt=enrolled.current_module.order)\
                    .order_by('order').first()
            except IndexError:
                self.message_user(request, 'User is already on the last course module', level='error')
            else:
                enrolled.current_module_id = module.pk
                enrolled.save()

                self.message_user(request, "User has been promoted to the next module", level='success')
            finally:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER',
                                                             reverse('admin:courses_enrolled_changelist') +
                                                             "?course_id={}".format(enrolled.course_id)))

    def enrolled_modules(self, request, enrolled_id, *args, **kwargs):
        pass

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('course_id'):
            return qs.filter(course_id=request.GET.get('course_id'))
        return qs

    def enrolled_actions(self, obj):
        return format_html('<a title="Promote to next module" href="{}"><i class="fa fa-caret-square-o-up"></i></a> '
                           '<a title="Open previous module" href="{}"><i class="fa fa-caret-square-o-down"></i></a> '
                           '<a title="Update payment" href="{}"><i class="fa fa-credit-card"></i></a>',
                           reverse('admin:promote-next-module', args=[obj.pk]), reverse('admin:enrolled-modules', args=[obj.pk]),
                           reverse('admin:courses_enrolled_changelist'))
    enrolled_actions.short_description = 'actions'
    enrolled_actions.allow_tags = True


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_fee', 'students_count', 'modules_count', 'is_active',
                    'created_by', 'created_at', 'course_actions')
    search_fields = ('name', )
    list_filter = ('created_by', 'created_at')
    exclude = ('slug', 'created_at', 'created_by', 'is_active')
    actions = ["mark_activated", "mark_deactivated"]

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
            re_path(
                r'^(?P<course_id>.+)/view/$',
                self.admin_site.admin_view(self.view_course),
                name='view',
            ),
        ]
        return custom_urls + urls

    def view_course(self, request, course_id, *args, **kwargs):
        course = self.get_object(request, course_id)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['course'] = course
        context['title'] = course.name
        return TemplateResponse(
            request,
            'admin/courses/view_course.html',
            context,
        )

    def view_students(self, request, course_id, *args, **kwargs):
        course = self.get_object(request, course_id)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['course'] = course
        return TemplateResponse(request, 'admin/courses/view_students.html', context)

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
                    self.message_user(request, 'Module created successfully', level='success')
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
        return format_html('<a title="View Course" href="{}"><i class="fa fa-eye"></i></a>&nbsp;' 
                           '<a title="Add Module" href="{}"><i class="fa fa-plus-circle"></i></a>&nbsp;'                           
                           '<a title="View Students" href="{}"><i class="fa fa-users"></i></a>&nbsp;',
                           reverse('admin:view', args=[obj.pk]), reverse('admin:add-module', args=[obj.pk]),
                           reverse('admin:courses_enrolled_changelist') + "?course_id={}".format(obj.pk))

    def mark_activated(self, request, queryset):
        queryset.update(is_active=True)

    def mark_deactivated(self, request, queryset):
        queryset.update(is_active=False)

    course_actions.short_description = 'Actions'
    course_actions.allow_tags = True


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'order', 'access_code', 'created_by', 'created_at')
    search_fields = ['name', 'course__name']
    list_filter = ('created_by', 'created_at', 'course')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


admin.site.register(Courses, CourseAdmin)
admin.site.register(Modules, ModuleAdmin)
admin.site.register(Enrolled, EnrolledAdmin)