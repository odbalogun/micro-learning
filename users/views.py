from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import UserModelForm, ChangePasswordForm
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
    form_class = ChangePasswordForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:change-password")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get('new_password'))
        user.save()
        update_session_auth_hash(self.request, user)

        messages.success(self.request, message="Your password has been changed successfully")
        return super().form_valid(form)


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