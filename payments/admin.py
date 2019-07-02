from django.contrib import admin
from .models import PaymentLog


class PaymentLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(PaymentLog, PaymentLogAdmin)