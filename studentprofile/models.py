from django.db import models
from django.contrib.auth.models import User


from login.models import Course

# Create your models here.
class Schedule(models.Model):
    # name = models.CharField(max_length=128)
    courses = models.ManyToManyField(Course, through='Class')

    def __str__(self):
        mylist = []
        for c in self.courses.all():
            myclass = Class.objects.get(schedule=self, course=c)
            mylist.append((str(c), myclass.strength))
        return str(mylist)

class Class(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    strength = models.PositiveSmallIntegerField()

class Student(models.Model):

    # Attach user as part of the model so that the user stores this information
    # in their profile
    user = models.OneToOneField(User,
                                on_delete = models.CASCADE) #If user is deleted, all fields are too

    name = models.CharField(max_length=100) # Field for user's name

    year = models.IntegerField(default = 1) # Field for user's year

    major = models.CharField(max_length=100, default = "None") # Field for user's major

    schedule = models.OneToOneField(Schedule, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return self.user.username
