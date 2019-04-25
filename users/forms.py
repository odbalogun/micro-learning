from django import forms
from django.conf import settings


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class UserModelForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField()
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = '__all__'
