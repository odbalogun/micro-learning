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
    enrolled = models.ForeignKey(Enrolled, on_delete=models.SET_NULL, blank=True, null=True)
    amount_paid = models.DecimalField('amount paid', decimal_places=2, max_digits=10, default=0)
    payment_type = models.CharField('payment type', max_length=50, choices=PAYMENT_TYPE_CHOICES, default='stripe')
    reference_no = models.CharField('reference no', max_length=50, blank=True, null=True)
    note = models.TextField('note', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)

    def course_name(self):
        return self.enrolled.course

    def user_name(self):
        return self.enrolled.user

    def display_amount_paid(self):
        return "${:0,.2f}".format(self.amount_paid)

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'

    reference_no.short_description = 'Payment Reference'
    display_amount_paid.short_description = 'Amount Paid'
