from .models import Courses, Modules
from rest_framework import serializers


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
