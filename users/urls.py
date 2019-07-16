from django.urls import path
from .views import UserLoginView, UserCreateView, UserListView, LogoutPageView, UserChangePasswordView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('create/', UserCreateView.as_view(), name='create'),
]
