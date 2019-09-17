from .models import Courses, Modules
from rest_framework import viewsets
from .serializers import CourseSerializer


class CourseApiViewSet(viewsets.ModelViewSet):
    """
    Endpoint to allow courses to be viewed on frontend
    """
    queryset = Courses.objects.filter(is_active=True)
    serializer_class = CourseSerializer
