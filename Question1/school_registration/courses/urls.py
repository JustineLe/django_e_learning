from django.urls import path

from .views import CourseList, CourseDetail, CourseEnrolledStudents

urlpatterns = [
    path('', CourseList.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('<int:pk>/enrolled/', CourseEnrolledStudents.as_view(), name='enrolled-students'),
]
