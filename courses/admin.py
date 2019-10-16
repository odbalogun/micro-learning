from django.contrib import admin
from django.urls import re_path, reverse
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, JsonResponse
from .models import Courses, Modules, Enrolled, EnrolledModules
from .forms import ModuleForm, OpenEnrolledModuleForm, EnrolledForm
from .tasks import set_current_module
from payments.forms import PaymentForm
from payments.admin import PaymentLogInline
from super_inlines.admin import SuperInlineModelAdmin


class EnrolledInline(SuperInlineModelAdmin, admin.StackedInline):
    model = Enrolled
    extra = 1
    can_delete = True
    inlines = (PaymentLogInline, )
    form = EnrolledForm


class EnrolledAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'current_module', 'status', 'payment_status', 'date_enrolled', 'enrolled_actions')
    search_fields = ['user__first_name', 'user__last_name', 'course__name']
    inlines = (PaymentLogInline, )
    form = EnrolledForm

    class Media:
        js = ("update_course_fee.js", )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
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
                r'^(?P<enrolled_id>.+)/promote-next-module/$',
                self.admin_site.admin_view(self.promote_next_module),
                name='promote-next-module',
            ),
            re_path(
                r'^(?P<enrolled_id>.+)/enrolled-modules/$',
                self.admin_site.admin_view(self.enrolled_modules),
                name='enrolled-modules',
            ),
            re_path(
                r'^(?P<enrolled_id>.+)/completed-course/$',
                self.admin_site.admin_view(self.completed_course),
                name='completed-course',
            ),
            re_path(
                r'^(?P<enrolled_id>.+)/add-payment/$',
                self.admin_site.admin_view(self.process_add_payment),
                name='add-payment',
            ),
        ]
        return custom_urls + urls

    def promote_next_module(self, request, enrolled_id, *args, **kwargs):
        enrolled = self.get_object(request, enrolled_id)
        if enrolled:
            # get next module
            if enrolled.current_module:
                order = enrolled.current_module.order
            else:
                order = 0

            module = Modules.objects.filter(course_id=enrolled.course_id, order__gt=order).order_by('order').first()
            if not module:
                self.message_user(request, 'User is already on the last course module', level='error')
            else:
                enrolled.current_module_id = module.pk
                enrolled.save()

                # save
                set_current_module(module, enrolled)

                self.message_user(request, "User has been promoted to the next module", level='success')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER',
                                                         reverse('admin:courses_enrolled_changelist') +
                                                         "?course_id={}".format(enrolled.course_id)))

    def enrolled_modules(self, request, enrolled_id, *args, **kwargs):
        enrolled = self.get_object(request, enrolled_id)

        if request.method != 'POST':
            form = OpenEnrolledModuleForm(initial={'enrolled': enrolled.id, 'user': enrolled.user_id, 'expires': 7})
        else:
            form = OpenEnrolledModuleForm(request.POST, initial={'enrolled': enrolled.id,
                                                                 'user': enrolled.user_id, 'expires': 7})
            if form.is_valid():
                form.save()
                enrolled.current_module = form.cleaned_data.get('module')
                enrolled.save()

                # set_current_module(module=Modules.objects.get)

                self.message_user(request, 'The user\'s module has been updated', level='success')
                url = reverse(
                    'admin:courses_enrolled_changelist',
                    current_app=self.admin_site.name,
                )
                return HttpResponseRedirect(url)

        form.fields['module'].queryset = Modules.objects.filter(course_id=enrolled.course_id)
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['enrolled'] = enrolled
        context['title'] = "Open Specific Module"
        return TemplateResponse(
            request,
            'admin/enrolled/view_modules.html',
            context,
        )

    def process_add_payment(self, request, enrolled_id, *args, **kwargs):
        return self.process_payment_form(
            request=request,
            enrolled_id=enrolled_id,
            action_form=PaymentForm,
            action_title='Add Payment',
        )

    def process_payment_form(self, request, enrolled_id, action_form, action_title):
        enrolled = self.get_object(request, enrolled_id)

        if enrolled.payment_status == 'paid':
            self.message_user(request, 'Full payment has already been made', level='error')
            url = reverse(
                'admin:courses_enrolled_changelist',
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(url)

        if enrolled.last_payment:
            amount = enrolled.last_payment.amount_owed
        else:
            amount = float(enrolled.course.course_fee / 2)

        if request.method != 'POST':
            form = action_form(initial={'enrolled': enrolled_id, 'created_by': request.user.id, 'amount_paid': amount})
        else:
            form = action_form(request.POST, initial={'enrolled': enrolled_id, 'created_by': request.user.id,
                                                      'amount_paid': amount})

            if form.is_valid():
                try:
                    payment = form.save()
                    payment.amount_paid = amount
                    payment.amount_owed = None
                    payment.save(force_discount=True)

                    # updated enrolled
                    enrolled.payment_status = 'paid'
                    enrolled.save()
                except Exception as e:
                    print(form.errors)
                    print(e)
                else:
                    self.message_user(request, 'Payment created successfully', level='success')
                    url = reverse(
                        'admin:courses_enrolled_changelist',
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['enrolled'] = enrolled
        context['title'] = action_title
        return TemplateResponse(
            request,
            'admin/courses/add_payment.html',
            context,
        )

    def completed_course(self, request, enrolled_id, *args, **kwargs):
        enrolled = self.get_object(request, enrolled_id)
        if enrolled:
            enrolled.status = 'completed'
            enrolled.save()

            self.message_user(request, "Course status has been successfully updated", level='success')
        else:
            self.message_user(request, "Enrollment entry could not be found", level='error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin:courses_enrolled_changelist')))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('course_id'):
            return qs.filter(course_id=request.GET.get('course_id'))
        return qs

    def get_available_actions(self, obj):
        links = ''

        if obj.status != 'completed':
            # check if user's on last module
            module = Modules.objects.filter(course_id=obj.course_id,
                                            order__gt=obj.current_module.order).order_by('order').first()
            if module:
                links += '<a title="Promote to next module" href="{}"><i class="fa fa-caret-square-o-up"></i></a> '.\
                    format(reverse('admin:promote-next-module', args=[obj.pk]))

        links += '<a title="Open specific module" href="{}"><i class="fa fa-folder-open"></i></a> '\
            .format(reverse('admin:enrolled-modules', args=[obj.pk]))

        if obj.payment_status != 'paid':
            links += '<a title="Add payment" href="{}"><i class="fa fa-credit-card"></i></a> '\
                .format(reverse('admin:add-payment', args=[obj.pk]))

        if obj.status != 'completed':
            links += '<a title="Mark course as completed" href="{}"><i class="fa fa-check-square"></i></a> '.\
                format(reverse('admin:completed-course', args=[obj.pk]))

        return links

    def enrolled_actions(self, obj):
        return format_html(self.get_available_actions(obj))

    enrolled_actions.short_description = 'actions'
    enrolled_actions.allow_tags = True


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code', 'slug', 'display_base_fee', 'display_fee', 'students_count', 'modules_count', 'is_active',
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
            re_path(
                r'^(?P<course_id>.+)/get-course/$',
                self.admin_site.admin_view(self.get_course_details),
                name='get-course',
            ),
        ]
        return custom_urls + urls

    def get_course_details(self, request, course_id, *args, **kwargs):
        course = self.get_object(request, course_id)
        return JsonResponse({"name": course.name, "course_fee": course.course_fee }, status=200)

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
        return format_html('<a title="Add Module" href="{}"><i class="fa fa-plus-circle"></i></a>&nbsp;'                           
                           '<a title="View Students" href="{}"><i class="fa fa-users"></i></a>&nbsp;',
                           reverse('admin:add-module', args=[obj.pk]), reverse('admin:courses_enrolled_changelist')
                           + "?course_id={}".format(obj.pk))

    def mark_activated(self, request, queryset):
        queryset.update(is_active=True)

    def mark_deactivated(self, request, queryset):
        queryset.update(is_active=False)

    course_actions.short_description = 'Actions'
    course_actions.allow_tags = True


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'order', 'access_code', 'created_by', 'created_at')
    search_fields = ['name', 'course__name']
    exclude = ('created_at', 'created_by')
    list_filter = ('created_by', 'created_at', 'course')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


admin.site.register(Courses, CourseAdmin)
admin.site.register(Modules, ModuleAdmin)
admin.site.register(Enrolled, EnrolledAdmin)