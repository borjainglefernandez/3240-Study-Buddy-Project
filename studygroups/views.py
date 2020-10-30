from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from studentprofile.models import Schedule, Course, Class, Student
from .models import StudyGroup
from django.contrib.auth.models import User

# Create your views here.
def makeGroup(request):
    user = User.objects.get(pk=request.user.id)

    # Error for if user name is null and the user is editing their profile
    null_name_error = render(request, 'studygroups/groupCreate.html', {  # Redirects the user to the profile page again
        'error_message': "Group name cannot be blank.",  # Description for the error message displayed
    })

    student = None
    try:
        student = Student.objects.get(user=request.user)
        if request.POST["Name"].strip() == "":
            return null_name_error  # cannot have an empty group name
    except:
        return HttpResponseRedirect(reverse('home'))

    #print("start of creation")
    studyGroup = StudyGroup(name=request.POST["Name"], maxSize=request.POST["Size"])
    studyGroup.save()
    studyGroup.members.add(student)
    studyGroup.save()
    #print("end of creation")

    return HttpResponseRedirect(reverse('home'))
