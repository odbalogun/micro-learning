from django.contrib import admin
from .models import Discount
from .forms import DiscountForm


class DiscountAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'created_by', 'is_active')
    list_display = ('code', 'display_amount', 'display_percentage', 'is_active', 'created_by', 'created_at')
    actions = ["activate", "deactivate"]
    form = DiscountForm

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

    def activate(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

    def display_percentage(self, obj):
        if obj.percentage:
            return "{}%".format(obj.percentage)
        return obj.percentage

    def display_amount(self, obj):
        if obj.amount:
            return "${:0,.2f}".format(obj.amount)
        return obj.amount

    activate.short_description = 'Activate selected discounts'
    deactivate.short_description = 'Deactivate selected discounts'

    display_percentage.admin_order_field = 'percentage'
    display_percentage.short_description = 'Percentage'

    display_amount.admin_order_field = 'amount'
    display_amount.short_description = 'Amount'


admin.site.register(Discount, DiscountAdmin)