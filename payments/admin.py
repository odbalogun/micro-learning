from django.contrib import admin
from .models import PaymentLog
from .forms import PaymentInlineForm
from django.urls import resolve
from django.contrib.admin.models import LogEntry
from super_inlines.admin import SuperInlineModelAdmin


class PaymentLogInline(SuperInlineModelAdmin, admin.StackedInline):
    model = PaymentLog
    extra = 1
    can_delete = False
    max_num = 1
    min_num = 1
    form = PaymentInlineForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.args:
            return self.parent_model.objects.get(pk=resolved.args[0])
        return None


class PaymentLogAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'created_at', 'reference_no', 'amount_owed', 'has_applied_discount')
    list_display = ['course_name', 'user_name', 'reference_no', 'payment_reference', 'payment_type',
                    'display_amount_paid', 'display_discount', 'display_amount_owed', 'created_at']
    list_display_links = None

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PaymentLogAdmin, self).get_actions(request)
        actions.pop('delete_selected', None)
        return actions


class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
                       'user',
                       'action_time',
                       'object_id',
                       'object_repr',
                       'action_flag',
                       'change_message'
                       )
    list_display = ['__str__', 'object_repr', 'content_type', 'user', 'action_time']
    list_display_links = None

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        actions.pop('delete_selected', None)
        return actions


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(PaymentLog, PaymentLogAdmin)