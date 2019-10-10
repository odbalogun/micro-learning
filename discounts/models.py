from django.db import models
from django.conf import settings


class Discount(models.Model):
    code = models.CharField('discount code', unique=True, null=False, max_length=100)
    amount = models.DecimalField('amount', decimal_places=2, max_digits=10, blank=True, null=True)
    percentage = models.IntegerField('percentage', blank=True, null=True)
    is_active = models.BooleanField('is active', default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)

    def __str__(self):
        return self.code
