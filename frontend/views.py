from django.shortcuts import render
from django.views.generic import FormView, CreateView, ListView


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    success_url = settings.LOGIN_REDIRECT_URL