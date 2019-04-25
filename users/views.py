from django.views.generic import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, UserModelForm


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"


class UserCreateView(CreateView):
    form_class =  UserModelForm
    template_name = "users/create.html"