from django.urls import path
from .views import LoginView, UserCreateView, UserListView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/', UserCreateView.as_view(), name='create'),
]
