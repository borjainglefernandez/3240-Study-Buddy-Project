from django.db import models
from django.contrib.auth.models import User


from login.models import Course

# Create your models here.
class Schedule(models.Model):
    # name = models.CharField(max_length=128)
    courses = models.ManyToManyField(Course, through='Class')
    #num = models.PositiveSmallIntegerField()
    

    # Create a list of all classes in a schedule so that
    # the template can run a for loop through
    def get_classes(self):
        classes = []
        for c in self.courses.all():
            myclass = Class.objects.get(schedule=self, course=c)
            classes.append(myclass)
        return classes

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

    def __str__(self):
        return str(self.course)

class Student(models.Model):

    # Attach user as part of the model so that the user stores this information
    # in their profile
    user = models.OneToOneField(User,
                                on_delete = models.CASCADE) #If user is deleted, all fields are too

    name = models.CharField(max_length=100) # Field for user's name

    year = models.PositiveSmallIntegerField(default = 1) # Field for user's year

    major = models.CharField(max_length=100, default = "None") # Field for user's major

    num = models.PositiveSmallIntegerField(default = 1) # Field for user's number of classes

    schedule = models.OneToOneField(Schedule, on_delete=models.SET_NULL, null=True)

    edit = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

