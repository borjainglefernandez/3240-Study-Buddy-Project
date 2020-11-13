from django.db import models

from studentprofile.models import Student
from login.models import Course

GROUPME_TOKEN = "0vlhRZGIYVOYuz7DJfBwTRdStaxXBIoEc7usZSJW"
from groupy.client import Client
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

    # https://stackoverflow.com/questions/1471909/django-model-delete-not-triggered
    def delete(self, *args, **kwargs):
        # Note this is a simple example. it only handles delete(),
        # and not replacing images in .save()
        print("deleting")
        group_id = None
        if (self.zoom != None):
            if (self.zoom.group_id != None):
                group_id = self.zoom.group_id

        super(StudyGroup, self).delete(*args, **kwargs)

        if (group_id != None):
                # Generate client that does the work
                client = Client.from_token(GROUPME_TOKEN)

                # Get group
                try:
                    group = client.groups.get(group_id)
                except:
                    print("Failed to find group")
                    return
                print("destroying group")
                group.destroy()