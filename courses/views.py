from django.views.generic import FormView, CreateView, ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from .models import Courses, Enrolled


# Create your views here.
class MyCoursesView(ListView):
    template_name = "courses/my_courses_list.html"
    queryset = Enrolled.objects.all()

    def get_queryset(self):
        return Enrolled.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class MyCertificatesView(ListView):
    template_name = 'courses/my_certificates_list.html'
    queryset = Enrolled.objects.all()

    def get_queryset(self):
        return Enrolled.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
