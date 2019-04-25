from django.urls import path
from .views import LoginView, UserCreateView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create/', UserCreateView.as_view(), name='create'),
]
