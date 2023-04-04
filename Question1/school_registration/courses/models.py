from django.db import models


class Courses(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    max_seats = models.IntegerField()
    enrollment_due_date = models.DateTimeField()

    def __str__(self):
        return self.name
