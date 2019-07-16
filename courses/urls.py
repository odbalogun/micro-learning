from django.urls import path
from .views import MyCoursesView, MyCertificatesView

app_name = 'courses'

urlpatterns = [
    path('my-courses', MyCoursesView.as_view(), name='my-courses'),
    path('my-certificates', MyCertificatesView.as_view(), name='my-certificates'),
]
