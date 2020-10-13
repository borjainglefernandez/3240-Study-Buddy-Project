# Watkins, jmw4dx
from django.http import HttpResponseRedirect, HttpResponse
from studentprofile.models import Student, Schedule, Course, Class
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse


def home(request):
    return HttpResponse("Hello, world! You're at the site.")

def submit_profile(request):
    # Fetch the current user
    user = User.objects.get(pk=request.user.id)

    # Create a Student Object that connects to that user
    student = Student(user = user, name = request.POST['Name'], year = request.POST['Year'], major = request.POST['Major'])

    # Create a Schedule Object with the number entered by user
    #schedule = Schedule(num=request.POST.get('NumClass'))

    # Save the Student Object we have just created
    student.save()
    #schedule.save()

    # Redirect to the schedule making page
    return HttpResponseRedirect(reverse('studentprofile:newSchedule')) 

class ProfileView(generic.TemplateView):
    model = Student
    template_name = 'studentprofile.html'

