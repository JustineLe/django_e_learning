from django.urls import path
from .views import StudentEnrollment, StudentDrop, EnrollmentDropStatistic

urlpatterns = [
    path('enroll/', StudentEnrollment.as_view(), name='student-enroll'),
    path('drop/', StudentDrop.as_view(), name='student-drop'),
    path('statistic/', EnrollmentDropStatistic.as_view(), name='student-drop'),
]