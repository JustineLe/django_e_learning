from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F, Count
from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.serializers import CourseSerializer, EnrolledStudentSerializer
from users.permissions import IsAdminUser
from .models import Courses

User = get_user_model()


class CourseList(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Courses.objects.annotate(enrolled_seats=Count("enrollment_course"))
        if not self.request.user.is_admin:
            now = timezone.now()
            queryset = queryset.filter(
                enrolled_seats__lt=F("max_seats"),
                enrollment_due_date__gt=now,
            )
        return queryset.all()

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Courses.objects.create(**serializer.validated_data)
        return Response(
            {'success': 'Course created successfully.'},
            status=status.HTTP_201_CREATED
        )


class CourseDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    def get_object(self, pk):
        queryset = Courses.objects.filter(pk=pk).annotate(enrolled_seats=Count("enrollment_course"))
        if not self.request.user.is_admin:
            now = timezone.now()
            queryset = queryset.filter(
                enrolled_seats__lt=F("max_seats"),
                enrollment_due_date__gt=now,
            )
        if not queryset.first():
            raise Http404
        return queryset.first()

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseEnrolledStudents(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk, format=None):
        queryset = User.objects.prefetch_related("enrollment_student").annotate(course_id=F("enrollment_student__course_id")).filter(course_id=pk)
        serializer = EnrolledStudentSerializer(queryset.all(), many=True)
        return Response(serializer.data)
