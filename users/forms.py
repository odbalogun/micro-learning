from django import forms
from .models import User


class UserModelForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField()
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password'
        ]


class LoginForm(forms.Form):
    username = forms.EmailField(required=True, max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = [
            'first_name', 'last_name', 'email', 'password', 'created_by'
        ]
