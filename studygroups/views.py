from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from studentprofile.models import Schedule, Course, Class, Student
from .models import StudyGroup
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def makeGroup(request):

    # Error for if user name is null and the user is editing their profile
    null_name_error = render(request, 'studygroups/groupCreate.html', {  # Redirects the user to the profile page again
        'error_message': "Group name cannot be blank.",  # Description for the error message displayed
    })

    repeated_name_error = render(request, 'studygroups/groupCreate.html', {  
        'error_message': "Group name is taken, please try another name",  # Description for the error message displayed
    })

    try:
        student = Student.objects.get(user=request.user)
        if request.POST["Name"].strip() == "":
            return null_name_error  # cannot have an empty group name
    except:
        return HttpResponseRedirect(reverse('home'))

    try:
        if StudyGroup.objects.get(name=request.POST["Name"]):
            return repeated_name_error
    except:
        print("All good!")

    studyGroup = StudyGroup(name=request.POST["Name"], maxSize=request.POST["Size"])
    studyGroup.save()
    studyGroup.members.add(student)
    studyGroup.save()
    
    # After a group is created, redirect the users to the group page
    context = {
        'StudyGroup':studyGroup,
        "members": studyGroup.members
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

    # Add student to group
    studyGroup.members.add(student)
    studyGroup.save()


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


    return HttpResponseRedirect(reverse('home'))

# Creates a dynamic view page for each group
def studygroup_detail(request, StudyGroup_name):
    try: 
        studygroup = StudyGroup.objects.get(name= StudyGroup_name)
        
    except StudyGroup.DoesNotExist:
        return HttpResponseRedirect(reverse('home'))
    
    print(StudyGroup_name)
    context = {
        "StudyGroup":studygroup,
        "members": studygroup.members
    }
    # Refers to the group page html
    return render(request, 'grouppage.html', context)

