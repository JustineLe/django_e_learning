from rest_framework import serializers
from .models import Courses


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = ["id", "name", "description", "max_seats", "enrollment_due_date", "enrolled_seats"]

    enrolled_seats = serializers.IntegerField(read_only=True)


class EnrolledStudentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
