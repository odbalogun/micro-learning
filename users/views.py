from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"

