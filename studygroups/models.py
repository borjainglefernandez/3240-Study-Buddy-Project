from django.db import models

from studentprofile.models import Student
from login.models import Course

GROUPME_TOKEN = "0vlhRZGIYVOYuz7DJfBwTRdStaxXBIoEc7usZSJW"
# Create your models here.
class ZoomInfo(models.Model):
    code = models.CharField(max_length=15, null=True)
    url = models.CharField(max_length=100, null=True)
    group_id = models.CharField(max_length=15, null=True)
    def __str__(self):
        return str(self.code) + " " + str(self.url) + " " + "Group Me ID: " + str(self.group_id)

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    maxSize = models.PositiveSmallIntegerField(default = 2)
    members = models.ManyToManyField(Student)
    zoom = models.OneToOneField(ZoomInfo, on_delete = models.DO_NOTHING, null = True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True)

    def get_members(self):
        members = list(self.members.all())
        return members

    #A method that prints only the name of the member in a group
    def get_members_string(self):
        members = list(self.members.all())
        string_members = ""

        # We do this so that the last element does not have a comma
        for i, member in enumerate(members):
            if i:
                string_members += ", "
            string_members += str(member)
        return string_members

    # A method that prints the name & email of the member in a group
    def get_members_email(self):
        members = list(self.members.all())
        string_members_email = ""

        # We do this so that the last element does not have a comma
        for i, member in enumerate(members):
            if i:
                string_members_email += ", "
            string_members_email += str(member)+" (" + str(member.get_email()) + ")"
        return string_members_email
    
    def __str__(self):
        return self.name + ": " + str([str(m) for m in self.members.all()])