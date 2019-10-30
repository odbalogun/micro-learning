from .models import Courses, Modules, PendingEnrollments
from rest_framework import serializers
from discounts.models import Discount


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Courses
        fields = ['id', 'name', 'course_code', 'slug', 'image', 'short_description', 'overview', 'outline',
                  'pre_requisites', 'strategy', 'tools_and_technology', 'learning_and_outcome', 'course_fee', 'modules']


class NewEnrolleeSerializer(serializers.ModelSerializer):
    discount_code = serializers.CharField(required=False)

    class Meta:
        model = PendingEnrollments
        exclude = ['date_created']

    def create(self, validated_data):
        discount_code = validated_data.pop('discount_code', None)

        if not discount_code:
            return PendingEnrollments.objects.create(**validated_data)
        else:
            discount = Discount.objects.filter(code=discount_code).first()

            if discount:
                return PendingEnrollments.objects.create(discount=discount, **validated_data)
            else:
                return PendingEnrollments.objects.create(**validated_data)