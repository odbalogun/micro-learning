from django.db import models
from django.conf import settings
from courses.models import Courses, Enrolled


# Create your models here.
class PaymentLog(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_log')
    amount_paid = models.DecimalField('amount paid', decimal_places=2, max_digits=10, default=0)
    note = models.TextField('note', null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
