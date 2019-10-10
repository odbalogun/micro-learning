from django.contrib import admin
from .models import PaymentLog
from django.contrib.admin.models import LogEntry


class PaymentLogAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'created_at')
    list_display = ['id', 'course_name', 'user_name', 'reference_no', 'display_amount_paid', 'payment_type', 'created_at']
    list_display_links = None

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

    def has_delete_permission(self, request, obj=None):
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