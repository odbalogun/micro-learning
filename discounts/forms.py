from django import forms
from .models import Discount


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        exclude = ('created_at', 'created_by', 'is_active')

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('percentage') and cleaned_data.get('amount'):
            raise forms.ValidationError("Provide either an amount or a percentage, not both.")

        if cleaned_data.get('percentage') is None and cleaned_data.get('amount') is None:
            raise forms.ValidationError("Please provide an amount or a percentage.")

    def clean_percentage(self):
        data = self.cleaned_data.get('percentage')

        if data:
            if data <= 0 or data >= 100:
                raise forms.ValidationError("Please provide a percentage between 1 and 100.")

        return data
