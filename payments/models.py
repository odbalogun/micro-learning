from django.db import models
from django.conf import settings
from courses.models import Enrolled


PAYMENT_TYPE_CHOICES = (
    ('stripe', 'Stripe'),
    ('bank-transfer', 'Bank Transfer'),
    ('cheque', 'Cheque'),
    ('other', 'Other'),
)


# Create your models here.
class PaymentLog(models.Model):
    enrolled = models.ForeignKey(Enrolled, on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField('amount paid', decimal_places=2, max_digits=10, default=0)
    payment_type = models.CharField('payment type', max_length=50, choices=PAYMENT_TYPE_CHOICES, default='stripe')
    reference_no = models.CharField('reference no', max_length=50, null=True)
    note = models.TextField('note', null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
