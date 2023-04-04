from django.db import transaction
from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Courses
from enrollments.models import Enrollments, Drops
from enrollments.serializers import StudentEnrollmentSerializer, StudentDropSerializer, \
    EnrollmentDropStatisticSerializer
from users.permissions import IsAdminUser


class StudentEnrollment(APIView):
    permission_classes = (IsAuthenticated & ~IsAdminUser,)

    @transaction.atomic
    def post(self, request):
        serializer = StudentEnrollmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = serializer.validated_data["course_id"]
        if Enrollments.objects.filter(course_id=course_id, student_id=request.user.id).exists():
            raise ValidationError({"course_id": "This student already enrolled the course"})
        course = Courses.objects.filter(pk=course_id).annotate(enrolled_seats=Count("enrollment_course")).first()
        if course.enrolled_seats >= course.max_seats:
            raise ValidationError({"course_id": "Seats are full. You can not enroll the course"})

        data = {
            "course_id": course,
            "student_id": request.user,
        }
        Enrollments(**data).save()
        return Response(
            {'success': 'Successfully enrolled course'},
            status=status.HTTP_200_OK
        )


class StudentDrop(APIView):
    permission_classes = (IsAuthenticated & ~IsAdminUser,)

    @transaction.atomic
    def post(self, request):
        serializer = StudentDropSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = serializer.validated_data["course_id"]
        enrollment_query = Enrollments.objects.filter(course_id=course_id, student_id=request.user.id)
        if not enrollment_query.exists():
            raise ValidationError({"course_id": "This student has not enrolled for the course"})
        enrollment_query.first().delete()
        course = Courses.objects.filter(pk=course_id).first()
        data = {
            "course_id": course,
            "student_id": request.user,
        }
        Drops(**data).save()
        return Response(
            {'success': 'Successfully drop course'},
            status=status.HTTP_200_OK
        )


class EnrollmentDropStatistic(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        enrollment_statistic = Enrollments.objects.all()
        drop_statistic = Drops.objects.all()
        data = {
            "enrollments": enrollment_statistic,
            "drops": drop_statistic
        }
        serializer = EnrollmentDropStatisticSerializer(data)
        return Response(serializer.data)
