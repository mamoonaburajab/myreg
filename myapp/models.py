from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Student(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField()

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    prerequisites = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    capacity = models.IntegerField()
    schedule = models.OneToOneField('CourseSchedule', on_delete=models.SET_NULL, null=True)

class CourseSchedule(models.Model):
    days = models.CharField(max_length=50) 
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=10)


class StudentRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return self.user.username
    

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)