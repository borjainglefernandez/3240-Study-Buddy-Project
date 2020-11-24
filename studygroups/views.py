from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from studentprofile.models import Schedule, Course, Class, Student
from .models import StudyGroup, GROUPME_TOKEN
from django.contrib import messages
from django.contrib.auth.models import User
from groupy.client import Client
from groupy.api.memberships import Memberships
import time

#def groupMeGenerateGroup(studyGroup: StudyGroup):
def groupMeGenerateGroup(studyGroup):
    # Generate client that does the work
    client = Client.from_token(GROUPME_TOKEN)
    # Create the group itself
    new_group = client.groups.create(name=studyGroup.name)

    studyGroup.group_id = new_group.group_id
    studyGroup.save()

def groupMeJoinGroup(studyGroup, student: Student):
    # Generate client that does the work
    client = Client.from_token(GROUPME_TOKEN)

    # Get group object
    try:
        group = client.groups.get(studyGroup.group_id)
    except:
        print("Failed to find group")
        return
    # group = None
    # for g in client.groups.list_all():
    #     if str(g.name) == studyGroup.name:
    #         group = g

    # Fancy out-of-library technique to do what I want - add via phone number
    mship = group.get_membership()
    memberships = Memberships(mship.manager.session, group_id=group.group_id)
    member = {
        'nickname': str(student.name),
        'phone_number': str(student.phone)
    }
    memberships.add_multiple(member)
    time.sleep(0.1)
    try:
        group = client.groups.get(studyGroup.group_id)
    except:
        print("Failed to find group")
        return
    # Save their user id for later
    mem = None
    print(group.members)
    for m in group.members:
        print(str(m.nickname), str(student.name))
        if str(m.nickname) == str(student.name):
            mem = m
    studyGroup.save()
    try:
        print(type(mem))
        print(mem)
        print(mem.user_id)
        print(str(mem.user_id))
        if mem != None and mem != "None":
            student.groupme_id = str(mem.user_id)
            student.save()
    except:
        print("Failed to save")
        pass


def groupMeLeaveGroup(studyGroup: StudyGroup, student: Student):
    # Generate client that does the work
    client = Client.from_token(GROUPME_TOKEN)

    # Get group object
    try:
        group = client.groups.get(studyGroup.group_id)
    except:
        print("Failed to find group")
        return

    # Assumes their user_id is known
    mem = None
    for m in group.members:
        if str(m.user_id) == str(student.groupme_id):
            mem = m
    try:
        mem.remove()
        mem.save()
    except:
        pass



# Create your views here.
def makeGroup(request):

    # Error for if user name is null and the user is editing their profile
    null_name_error = render(request, 'studygroups/groupCreate.html', {  # Redirects the user to the group creation page again
        'error_message': "Group name cannot be blank.",  # Description for the error message displayed
    })

    repeated_name_error = render(request, 'studygroups/groupCreate.html', {
        'error_message': "Group name is taken, please try another name",  # Description for the error message displayed
    })

    # Error for if class number is not a digit
    class_number_digit_error = render(request, 'studygroups/groupCreate.html', {
        'error_message': "Class number must be a digit.",
    })

    # Error for if class number is not 4 digits
    class_number_length_error = render(request, 'studygroups/groupCreate.html', {
        'error_message': "Class number must be 4 digits.",
    })

    # Error for if class is not formatted correctly
    class_input_error = render(request, 'studygroups/groupCreate.html', {
        'error_message': "Class must be a course mnemonic (i.e. CS) followed by a space followed by a 4 digit number (i.e. 3240).",
    })

    # Error for if a course inputted does not exist
    course_does_not_exist_error = render(request, 'studygroups/groupCreate.html', {
        'error_message': "The course inputted does not exist.",
    })

    # Error for if there are not enough classes inputted
    not_enough_classes_error = render(request, 'studygroups/groupCreate.html', {
        'error_message': "You are missing the required course field.",
    })
    
    # Error for if there's a '/' in the name (or it will mess up the urls)
    name_slash_error = render(request, 'studygroups/groupCreate.html', {
        'error_message': "Group name can not contain characters like '/'.",
    })

    try:
        student = Student.objects.get(user=request.user)
        if request.POST["Name"].strip() == "":
            return null_name_error  # cannot have an empty group name
    except:
        return HttpResponseRedirect(reverse('home'))

    try:
        if '/' in request.POST["Name"].strip():
            return name_slash_error 
    except:
        print("All good!")
        
    try:
        if StudyGroup.objects.get(name=request.POST["Name"].strip()):
            return repeated_name_error
    except:
        print("All good!")

    # allowedCharacters = "ABCDEFGHabcdef1234567890!@#$^&*() _-=+"
    # for c in request.POST["Name"]:
    #     if c not in allowedCharacters:
    #         return ERROR

    courseParts = request.POST["Class"].strip().split(" ")

    if len(courseParts) == 2:
        mn = courseParts[0]
        num = courseParts[1]

        # If the number inputted for the class is not 4 digits, raise an error
        if len(num) != 4:
            return class_number_length_error

        # If the number inputted for the class is not a digit, raise an error
        elif not num.isdigit():
            return class_number_digit_error

        else:
            try:
                course = Course.objects.get(mnemonic=mn, number=int(num))

            # If the inputted course is in a valid format but does not exist, raise an error
            except Course.DoesNotExist:
                return course_does_not_exist_error

    # If one or more class field is blank, raise an error
    elif request.POST["Class"] == '':
        return not_enough_classes_error

    # If class is not formatted correctly, raise an error
    else:
        return class_input_error

    studyGroup = StudyGroup(name=request.POST["Name"].strip(), maxSize=request.POST["Size"], course= course)
    studyGroup.save()
    studyGroup.members.add(student)
    studyGroup.save()
    groupMeGenerateGroup(studyGroup)
    studyGroup.save()
    groupMeJoinGroup(studyGroup, student)
    
    # After a group is created, redirect the users to the group page
    context = {
        'StudyGroup':studyGroup,
    }
    return render(request, 'grouppage.html', context)

def joinGroup(request):

    try:
        student = Student.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('home'))

    # Obtain the study group based on the id
    studyGroup = StudyGroup.objects.get(pk = int(request.POST['Group']))
    studyGroup.save()

    if studyGroup.maxSize == len(studyGroup.get_members()):
        return HttpResponseRedirect(reverse('home'))

    # Add student to group
    studyGroup.members.add(student)
    studyGroup.save()


    if studyGroup.group_id != "None": # Assumed situation
        groupMeJoinGroup(studyGroup, student)
    else: # Panic situation
        groupMeGenerateGroup(studyGroup)
        for s in studyGroup.members.all():
            groupMeJoinGroup(studyGroup, s)

    return HttpResponseRedirect(reverse('home'))

def leaveGroup(request):

    try:
        student = Student.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('home'))

    # Obtain the study group based on the id
    studyGroup = StudyGroup.objects.get(pk = int(request.POST['Group']))
    studyGroup.save()

    # Remove student from group
    studyGroup.members.remove(student)
    studyGroup.save()

    if studyGroup.group_id != "None": # Assumed situation
        groupMeLeaveGroup(studyGroup, student)
    else: # Panic situation
        groupMeGenerateGroup(studyGroup)
        for s in studyGroup.members.all():
            groupMeJoinGroup(studyGroup, s)

    if str(studyGroup.get_members_string()) == "":
        studyGroup = StudyGroup.objects.get(pk=int(request.POST['Group']))
        studyGroup.delete()

    return HttpResponseRedirect(reverse('home'))

# Creates a dynamic view page for each group
def studygroup_detail(request, StudyGroup_name):
    try: 
        studygroup = StudyGroup.objects.get(name= StudyGroup_name)
        student = Student.objects.get(user=request.user)
        
    except StudyGroup.DoesNotExist or Student.DoesNotExist:
        return HttpResponseRedirect(reverse('home'))
    
    print(StudyGroup_name)
    context = {
        "StudyGroup":studygroup,
        "Student":student
    }
    # Refers to the group page html
    return render(request, 'grouppage.html', context)

