from django.db import models

from studentprofile.models import Student

# Create your models here.
class ZoomInfo(models.Model):
    code = models.CharField(max_length=15)

    def __str__(self):
        return self.code

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    maxSize = models.PositiveSmallIntegerField(default = 2)
    members = models.ManyToManyField(Student)
    zoom = models.OneToOneField(ZoomInfo, on_delete = models.DO_NOTHING, null = True)

    def __str__(self):
        return self.name + ": " + str([str(m) for m in self.members.all()])