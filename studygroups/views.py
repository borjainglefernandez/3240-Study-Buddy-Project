from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from studentprofile.models import Schedule, Course, Class, Student
from django.contrib.auth.models import User

# Create your views here.
def makeGroup(request):

    return HttpResponseRedirect(reverse('student profile'))
