from django.db import models

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