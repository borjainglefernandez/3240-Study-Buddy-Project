# Watkins, jmw4dx
from django.http import HttpResponseRedirect, HttpResponse
from studentprofile.models import Student, Schedule, Course, Class
from django.contrib.auth.models import User
from django.views import generic
from django.shortcuts import render, reverse


def home(request):
    return HttpResponse("Hello, world! You're at the site.")

def submit_profile(request):
    # Fetch the current user
    user = User.objects.get(pk=request.user.id)
    
    # Error for if user name is null
    null_name_error = render(request, 'login/index.html', { # Redirects the user to the profile page again
        'error_message': "Username cannot be blank.", # Description for the error message displayed
    })

    print(request.POST)
    if (request.POST['Name'] != "" and request.POST['Name'] != " "):
        # Tests if an object of Student model exists
        try:
            foo = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            foo = None

        if foo == None:
            # If the user doesn't exist, create a Student Object that connects to that user
            student = Student(user = request.user, name = request.POST['Name'], year = request.POST['Year'],
                    major = request.POST['Major'], num = request.POST["NumClass"])

            # Save the Student Object we have just created
            student.save()

        else:
            # If the user exists, update the profile
            foo.name = request.POST["Name"]
            foo.year = request.POST["Year"]
            foo.major = request.POST['Major']
            foo.num = request.POST["NumClass"]
            foo.save()

        # Create an array equivalent to the size of the number of classes a user wants to input
        num_of_classes = request.POST['NumClass']
        numC = []
        for i in range(0,int(num_of_classes)):
            numC.append(1) # Note that it does not matter what is in the array
                      # it just simply needs to be the size of the number of classes

        # This creates a dict for the template to be able to access num
        context = {'numC': numC}

    else: 
        # Prints the error message
        return null_name_error

                # This creates a dict for the template to be able to access num
                context = {'num': num}

                # Redirect to the schedule making page
                return render(request, 'studentprofile/schedule.html', context)
    else:
        print("no :( -----------------------------")

def edit_profile(request):
    student = Student.objects.get(user=request.user)
    student.edit = True
    print(student)
    student.save()
    return HttpResponseRedirect(reverse('student profile'))

class ProfileView(generic.TemplateView):
    model = Student
    template_name = 'studentprofile.html'

