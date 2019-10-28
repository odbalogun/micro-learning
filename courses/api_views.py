from .models import Courses, Modules, Enrolled
from rest_framework import viewsets, generics
from .serializers import CourseSerializer, NewEnrolleeSerializer
from rest_framework.response import Response
from rest_framework import status
from olade.utilities import random_string
from users.models import User


class CourseApiViewSet(viewsets.ModelViewSet):
    """
    Endpoint to allow courses to be viewed on frontend
    """
    queryset = Courses.objects.filter(is_active=True)
    serializer_class = CourseSerializer


class NewEnrolleeApiViewSet(viewsets.GenericViewSet):
    """
    Endpoint to create/register a new signup
    """
    serializer_class = NewEnrolleeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = Courses.objects.filter(pk=serializer.data.get('course_id')).first()

        if not course:
            return Response({'error': 'Selected course does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # if it does, check if user exists
        user = User.objects.filter(email=serializer.data.get('email')).first()

        if not user:
            token = random_string(8)
            data = serializer.data
            user = User.objects.create_student(email=data.get('email'), password=token,
                                               first_name=data.get('first_name'), last_name=data.get('last_name'),
                                               phone_number=data.get('phone_number'))

        # check if user has already enrolled
        check = Enrolled.objects.filter(user=user, course=course).first()

        if check:
            return Response({'error': 'You are already registered for this course'}, status=status.HTTP_409_CONFLICT)

        # add enrollment information
        print(course.get_first_module)
        enrollee = Enrolled(course=course, user=user, current_module=course.get_first_module, status='pending',
                            payment_status='unpaid')
        enrollee.save()
        return Response({'msg': 'Successfully registered', 'enrollee': enrollee.pk}, status=status.HTTP_201_CREATED)