from django.utils import timezone
from rest_framework import serializers

from courses.models import Courses
from enrollments.models import Enrollments, Drops


class StudentEnrollmentSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate(self, attrs):
        query_set = Courses.objects.filter(id=attrs['course_id'])
        if not query_set.exists():
            raise serializers.ValidationError({"course_id": f"The course with id {attrs['course_id']} doesn't exist"})
        course = query_set.first()
        now = timezone.now()
        if now > course.enrollment_due_date:
            raise serializers.ValidationError({"course_id": "The course has expired, you cannot register for this course"})
        return attrs


class StudentDropSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate(self, attrs):
        query_set = Courses.objects.filter(id=attrs['course_id'])
        if not query_set.exists():
            raise serializers.ValidationError({"course_id": f"The course with id {attrs['course_id']} doesn't exist"})
        return attrs


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollments
        fields = "__all__"


class DropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drops
        fields = "__all__"


class EnrollmentDropStatisticSerializer(serializers.Serializer):
    enrollments = EnrollmentSerializer(many=True)
    drops = DropSerializer(many=True)
