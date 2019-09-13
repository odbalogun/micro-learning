from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, FormView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import UserModelForm, ChangePasswordForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


class UserLoginView(LoginView):
    # form_class = LoginForm
    template_name = "users/login.html"
    success_url = settings.LOGIN_REDIRECT_URL
    redirect_authenticated_user = True

    def form_invalid(self, form):
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors()[0])
        return redirect(reverse_lazy("users:login"))


class RequestPasswordResetView(PasswordResetView):
    template_name = "users/request_password.html"
    success_url = reverse_lazy("users:request-password-reset")

    def form_invalid(self, form):
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors()[0])
        return redirect(reverse_lazy("users:request-password-reset"))

    def form_valid(self, form):
        # get user by email
        user = User.objects.filter(email=form.cleaned_data['email']).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(self.request)
            domain = current_site.domain
            user.email_user(subject="Request Password Reset", title="You have requested to reset your password",
                            subtitle="You have requested a password reset",
                            content="You're receiving this email because you requested a password reset for your "
                                    "Olade user account. \n Please go to the following page to choose a new password."
                                    "\n Kindly ignore this email if you did not request to reset your password",
                            button_value="Reset Password", button_link="http://{}{}".
                            format(domain, reverse_lazy("users:password-reset", kwargs={'uidb64': uid, 'token': token})))
            # send email
            messages.success(self.request, "A password reset email has been sent to you")
        else:
            messages.error(self.request, "This user does not exist")
        return redirect(reverse_lazy("users:request-password-reset"))


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = settings.LOGIN_REDIRECT_URL

    def form_invalid(self, form):
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors()[0])
        print(form.errors)
        print(form.non_field_errors())
        return super().form_invalid(form)

    def form_valid(self, form):
        print(form.errors)
        print(form.non_field_errors())
        messages.success(self.request, "Your password has been successfully reset")
        return super().form_valid(form)


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


class ProfileView(UpdateView):
    model = User
    template_name = 'users/my_profile.html'
    fields = ['first_name', 'last_name', 'phone_number', 'address', 'identity']
    success_url = reverse_lazy("users:my-profile")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, **kwargs)

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        messages.success(self.request, message="Your profile has been successfully updated")
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