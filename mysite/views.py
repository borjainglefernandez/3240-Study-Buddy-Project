# Watkins, jmw4dx
from django.http import HttpResponseRedirect, HttpResponse
from studentprofile.models import Student
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

    # Save the Student Object we have just created
    student.save()

    # Redirect to the student profile page
    return HttpResponseRedirect(reverse('student profile'))

class ProfileView(generic.TemplateView):
    model = Student
    template_name = 'studentprofile.html'

