from django.db import models
from django.conf import settings
from courses.models import Enrolled
from discounts.models import Discount


PAYMENT_TYPE_CHOICES = (
    ('stripe', 'Online Payment (Stripe)'),
    ('cash', 'Cash'),
    ('money-transfer', 'Money Transfer'),
    ('cheque', 'Cheque'),
    ('other', 'Other'),
)


def increment_reference_number():
    last_payment = PaymentLog.objects.all().order_by('id').last()
    if not last_payment:
        return 'OLAD00000001'
    reference_int = int(last_payment.reference_no.split('OLAD')[-1])
    return 'OLAD' + str(reference_int + 1).zfill(8)


# Create your models here.
class PaymentLog(models.Model):
    enrolled = models.ForeignKey(Enrolled, on_delete=models.SET_NULL, blank=True, null=True, related_name='payments')
    amount_paid = models.DecimalField('amount paid', decimal_places=2, max_digits=10)
    payment_type = models.CharField('payment type', max_length=50, choices=PAYMENT_TYPE_CHOICES, default='stripe',
                                    null=False)
    reference_no = models.CharField('reference no', max_length=50, null=False, unique=True,
                                    default=increment_reference_number)
    payment_reference = models.CharField('cheque no', max_length=50, unique=True, blank=True, null=True)
    applied_discount = models.DecimalField('discount', blank=True, null=True, decimal_places=2, max_digits=10)
    discount = models.ForeignKey(Discount, verbose_name='discount code', on_delete=models.SET_NULL, blank=True,
                                 null=True)
    amount_owed = models.DecimalField('amount owed', null=True, blank=True, decimal_places=2, max_digits=10)
    has_applied_discount = models.BooleanField('has applied discount', default=False)
    note = models.TextField('note', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)

    def __str__(self):
        return self.reference_no

    def _apply_discount(self):
        if self.discount:
            # check if percentage
            if self.discount.percentage:
                discount = float(self.amount_paid) * float(self.discount.percentage/100)
                self.amount_paid -= discount
                self.applied_discount = discount
            else:
                self.amount_paid = float(self.amount_paid) - float(self.discount.amount)
                self.applied_discount = self.discount.amount

    def course_name(self):
        return self.enrolled.course

    def user_name(self):
        return self.enrolled.user

    def display_amount_paid(self):
        if self.amount_paid:
            return "${:0,.2f}".format(self.amount_paid)
        return self.amount_paid

    def display_discount(self):
        if self.applied_discount:
            return "${:0,.2f}".format(self.applied_discount)
        return self.applied_discount

    def display_amount_owed(self):
        if self.amount_owed:
            return "${:0,.2f}".format(self.amount_owed)
        return self.amount_owed

    def save(self, *args, **kwargs):
        if not self.has_applied_discount or kwargs.get('force_discount', None):
            self._apply_discount()
            self.has_applied_discount = True
        kwargs.pop('force_discount', None)
        super(PaymentLog, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'

    reference_no.short_description = 'Payment Reference'
    display_amount_paid.short_description = 'Amount Paid'
    display_discount.short_description = 'Discount'
    display_amount_owed.short_description = 'Amount Owed'
