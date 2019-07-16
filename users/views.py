from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import UserModelForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class UserLoginView(LoginView):
    # form_class = LoginForm
    template_name = "users/login.html"
    success_url = settings.LOGIN_REDIRECT_URL
    redirect_authenticated_user = True

    def form_invalid(self, form):
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors()[0])
        else:
            messages.error(self.request, form.errors[0])
        return redirect(reverse_lazy("users:login"))


class UserChangePasswordView(FormView):
    form_class = SetPasswordForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:change-password")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs


class LogoutPageView(LogoutView):
    # template_name = 'users/logout.html'
    next_page = reverse_lazy("users:login")


class UserListView(ListView):
    template_name = "users/list.html"
    queryset = User.objects.all()


class UserCreateView(CreateView):
    form_class = UserModelForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        self.object = User.objects.create_user(email=form.cleaned_data['email'], password=form.cleaned_data['password'],
                                               first_name=form.cleaned_data['first_name'],
                                               last_name=form.cleaned_data['last_name'])
        return HttpResponseRedirect(self.get_success_url())