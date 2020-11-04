from django.db import models

from studentprofile.models import Student
from login.models import Course


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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True)

    def get_members(self):
        members = list(self.members.all())
        return members

    def get_members_string(self):
        members = list(self.members.all())
        string_members = ""

        # We do this so that the last element does not have a comma
        for i, member in enumerate(members):
            if i:
                string_members += ", "
            string_members += str(member)
        return string_members

    def __str__(self):
        return self.name + ": " + str([str(m) for m in self.members.all()])