from django.db import models
from courses.models import Courses
from users.models import Account


class Enrollments(models.Model):
    student_id = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="enrollment_student")
    course_id = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True, related_name="enrollment_course")
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Drops(models.Model):
    student_id = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="drop")
    course_id = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True, related_name="drop")
    drop_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
