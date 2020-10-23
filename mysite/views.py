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

    # Error for if user name is null and its the first time the user is logging in
    null_name_error_create = render(request, 'login/index.html', { # Redirects the user to the login page again
        'error_message': "Username cannot be blank.", # Description for the error message displayed
    })

    # Error for if user name is null and the user is editing their profile
    null_name_error_edit = render(request, 'studentprofile.html', {  # Redirects the user to the profile page again
        'error_message': "Username cannot be blank.",  # Description for the error message displayed
    })

    if request.method=='POST':
        first_time = False
        print(request.POST)

        try:
            student = Student.objects.get(user=request.user)

            if request.POST["Name"].strip() == "":
                return null_name_error_edit # if user is editing their profile and there is no name
                                            # raise the error

        except:
            if request.POST["Name"].strip() == "":
                return null_name_error_create # if user is creating their profile for first time and there is no name
                                              # raise the error
            # Create a Student Object that connects to that user
            student = Student(user = user, name = request.POST['Name'], year = request.POST['Year'],
                        major = request.POST['Major'], num = request.POST['NumClass'])
            first_time = True
            # Save the Student Object we have just created
            student.save()


        # If this is the first time the user is generating the schedule
        if 'generate-schedule' in request.POST and first_time:

            # Create an array equivalent to the size of the number of classes a user wants to input
            num_of_classes = request.POST['NumClass']
            num = []
            for i in range(0,int(num_of_classes)):
                num.append(1) # Note that it does not matter what is in the array
                            # it just simply needs to be the size of the number of classes

            # This creates a dict for the template to be able to access num
            context = {'numC': num}

            # Redirect to the schedule making page
            return render(request, 'studentprofile/schedule.html', context)

        # Otherwise 
        else:
            student.name = request.POST['Name']
            student.year = request.POST['Year']
            student.major = request.POST['Major']
            student.num = request.POST['NumClass']
            student.edit = False
            student.save()

            print(student.year, "year")

            if 'save-profile' in request.POST:
                print("HERE")
                return HttpResponseRedirect(reverse('student profile'))
            else:
                num_of_classes = student.num
                num = []
                for i in range(0,int(num_of_classes)):
                    num.append(1) # Note that it does not matter what is in the array
                                # it just simply needs to be the size of the number of classes

                # This creates a dict for the template to be able to access num
                context = {'numC': num}

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

