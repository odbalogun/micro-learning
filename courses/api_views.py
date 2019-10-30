from .models import Courses, Modules, Enrolled
from rest_framework import viewsets, generics
from .serializers import CourseSerializer, NewEnrolleeSerializer
from rest_framework.response import Response
from rest_framework import status
from olade.utilities import random_string
from users.models import User
from payments.models import PaymentLog


class CourseApiViewSet(viewsets.ModelViewSet):
    """
    Endpoint to allow courses to be viewed on frontend
    """
    queryset = Courses.objects.filter(is_active=True)
    serializer_class = CourseSerializer


class NewEnrolleeApiViewSet(viewsets.ModelViewSet):
    """
    Endpoint to create/register a new signup
    """
    serializer_class = NewEnrolleeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # if it does, check if user exists
        user = User.objects.filter(email=serializer.validated_data.get('email')).first()

        if not user:
            token = random_string(8)
            data = serializer.validated_data
            user = User.objects.create_student(email=data.get('email'), password=token,
                                               first_name=data.get('first_name'), last_name=data.get('last_name'),
                                               phone_number=data.get('phone_number'))
            # todo ensure welcome email is sent

        # check if user has already enrolled
        check = Enrolled.objects.filter(user=user, course=serializer.validated_data.get('course')).first()

        if check:
            return Response({'error': 'You are already registered for this course'}, status=status.HTTP_409_CONFLICT)

        instance = serializer.save()
        return Response({'msg': 'Successfully registered', 'enrollee': instance.pk}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.payment_status = 'paid'
        instance.save()

        # fetch user based off email
        user = User.objects.filter(email=instance.email).first()

        # create enrollment
        enrolled = Enrolled(course=instance.course, current_module=instance.course.get_first_module, user=user,
                            status='pending')
        enrolled.payment_status = 'partly' if instance.payment_type == 'partial' else 'paid'
        enrolled.save()

        # add new payment log
        # todo
        # check if full payment
        # set amount accordingly
        # add discount if exists
        # save
        payment = PaymentLog(enrolled=enrolled, payment_reference=request.data.get('payment_reference', None),
                             amount=request.data.get('amount', None))
        payment.save()
        # todo send email
        return Response({'msg': 'Successfully updated'}, status=status.HTTP_200_OK)