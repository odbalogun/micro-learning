from .models import PaymentLog, Refund, Enrolled
from django import forms


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentLog
        exclude = ('created_by', 'created_at', 'reference_no', 'applied_discount', 'amount_owed',
                   'has_applied_discount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_paid'].disabled = True
        self.fields['amount_paid'].label = 'Amount Owed'


class PaymentInlineForm(forms.ModelForm):
    class Meta:
        model = PaymentLog
        exclude = ('created_by', 'created_at', 'amount_paid', 'applied_discount', 'amount_owed', 'has_applied_discount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reference_no'].disabled = True

    def has_changed(self, *args, **kwargs):
        return True


class RefundForm(forms.ModelForm):
    amount_paid = forms.DecimalField(label='Amount Paid')

    class Meta:
        model = Refund
        exclude = ('created_at', 'created_by', 'enrolled', 'reference_no')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_paid'].disabled = True

    def clean_amount(self):
        enrolled = Enrolled.objects.get(pk=self.initial.get('enrolled'))
        amount = self.cleaned_data.get('amount')
        if enrolled:
            if amount > enrolled.total_amount_paid:
                raise forms.ValidationError('Error. Refund amount cannot be greater than amount paid (${})'.format(
                    enrolled.total_amount_paid))
            return amount
        raise forms.ValidationError('Invalid enrolled record provided')

    field_order = ['amount_paid', 'amount', 'note']
