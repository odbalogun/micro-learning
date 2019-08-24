from django.contrib import admin
from .models import PaymentLog


class PaymentLogAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'created_at')
    list_display = ['id', 'course_name', 'user_name', 'reference_no', 'amount_paid', 'payment_type', 'created_at']
    list_display_links = None

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


admin.site.register(PaymentLog, PaymentLogAdmin)