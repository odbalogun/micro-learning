from .models import PaymentLog
from django import forms


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentLog
        exclude = ('created_at', 'created_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrolled'].disabled = True