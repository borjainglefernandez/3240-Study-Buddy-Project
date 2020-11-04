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


    studyGroup = StudyGroup(name=request.POST["Name"], maxSize=request.POST["Size"], course= course)
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

