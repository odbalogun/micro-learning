from django.urls import path
from .views import MyCoursesView, MyCertificatesView, CourseView

app_name = 'courses'

urlpatterns = [
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('my-certificates/', MyCertificatesView.as_view(), name='my-certificates'),
    path('<pk>/', CourseView.as_view(), name='detail'),
]
