from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):

    # Attach user as part of the model so that the user stores this information
    # in their profile
    user = models.OneToOneField(User,
                                on_delete = models.CASCADE) #If user is deleted, all fields are too

    name = models.CharField(max_length=100) # Field for user's name

    year = models.IntegerField(default = 1) # Field for user's year

    major = models.CharField(max_length=100, default = "None") # Field for user's major

    def __str__(self):
        return self.user.username
