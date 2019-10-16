from .models import PaymentLog
from django import forms


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentLog
        exclude = ('created_by', 'created_at', 'reference_no', 'applied_discount', 'amount_owed',
                   'has_applied_discount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_paid'].disabled = True


class PaymentInlineForm(forms.ModelForm):
    class Meta:
        model = PaymentLog
        exclude = ('created_by', 'created_at', 'amount_paid', 'applied_discount', 'amount_owed', 'has_applied_discount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reference_no'].disabled = True

    def has_changed(self, *args, **kwargs):
        return True
