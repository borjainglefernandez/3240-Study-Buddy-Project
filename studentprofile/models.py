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

    phone = models.PositiveBigIntegerField(default=0)

    year = models.PositiveSmallIntegerField(default = 1) # Field for user's year

    major = models.CharField(max_length=100, default = "None") # Field for user's major

    num = models.PositiveSmallIntegerField(default = 1) # Field for user's number of classes

    schedule = models.OneToOneField(Schedule, on_delete=models.SET_NULL, null=True)

    groupme_id = models.CharField(max_length=15, default = "None")

    edit = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_email(self):
        return self.user.email

    # Obtains a student's classes in order of strength
    #
    # Sorts it in ascending order
    def get_classes_in_str_order(self):
        if self.schedule is None:
            return []

        result = []

        if self.schedule is None:
            return []

        classes = self.schedule.get_classes() # Get all of the students' classes in the schedule


        minstr = 9
        minclass = None

        while len(classes) > 0: # While there are classes left we haven't sorted
            for clas in classes:
                if clas.strength < minstr: # If class is the minimum strength
                    minstr = clas.strength
                    minclass = clas
            result.append(minclass) # Add minimum class found to the result
            classes.remove(minclass)
            minstr = 9

        return result

    def get_suggested_groups(self):
        from studygroups.models import StudyGroup # Doesn't work when I import it at the top (circular import)
        suggested_groups = []
        relevant_groups = []
        classes_sorted_by_str = self.get_classes_in_str_order() # Obtain students' classes in sorted order

        # Get all groups with a course that the student has in their schedule
        for group in StudyGroup.objects.all():
            # 1.) Check if the groups' course matches a course in a students' schedule
            # 2.) Check if the student is not already in the course
            # 3.) Check if the group is full or not
            if (str(group.course) in str(classes_sorted_by_str)) \
                    and not(self in group.get_members()) \
                    and not(len(group.get_members()) == group.maxSize):

                relevant_groups.append(group)

        # Sort relevant groups in order of suggestedness
        #
        # Iterate in order of strength of classes and see if a relevant class is found
        for clas in classes_sorted_by_str:
            for group in relevant_groups:
                if str(clas) == str(group.course):
                    suggested_groups.append(group)
                    
        # If we have more than 3 suggested groups, trim the list to only 3
        if len(suggested_groups) > 3:
            suggested_groups = suggested_groups[:3]

        return suggested_groups
    
    
    def get_available_groups(self):
        from studygroups.models import StudyGroup 
        available_groups = []
        relevant_groups = []
        suggested_groups = self.get_suggested_groups() # checks for repeated groups 
        classes_sorted_by_str = self.get_classes_in_str_order() # Obtain students' classes in sorted order

        # Get all groups with a course that the student has in their schedule
        for group in StudyGroup.objects.all():
            # 1.) Check if the groups' course matches a course in a students' schedule
            # 2.) Check if the group is full or not
            if (str(group.course) in str(classes_sorted_by_str)) \
                    and not(len(group.get_members()) == group.maxSize):
                relevant_groups.append(group)
            
            # Adds the group to available group if the user is in it,
            # even though the course does not match user's schedule
            elif self in group.get_members(): 
                available_groups.append(group)

        # Sort relevant groups in order of suggestedness
        #
        # Iterate in order of strength of classes and see if a relevant class is found
        for clas in classes_sorted_by_str:
            for group in relevant_groups:
                if str(clas) == str(group.course):
                    available_groups.append(group)
        
        # Do not show the same groups from the suggested group again in the available group
        for suggest in suggested_groups:
            for group in available_groups:
                if str(group) == str(suggest):
                    available_groups.remove(group)

        return available_groups




