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

    if request.method=='POST':
        first_time = False

        try:
            student = Student.objects.get(user=request.user)
        except:
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
            context = {'num': num}
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
            
            print(student.edit, "sched")
            print(student.name, "name1") # there is no name??
            print(not user.student.name, "name") # this check is failing
            print(user.student.edit, "edit")

            if 'save-profile' in request.POST:
                return HttpResponseRedirect(reverse('student profile'))
            else:
                num_of_classes = student.num
                num = []
                for i in range(0,int(num_of_classes)):
                    num.append(1) # Note that it does not matter what is in the array
                                # it just simply needs to be the size of the number of classes

                # This creates a dict for the template to be able to access num
                context = {'num': num}

                # Redirect to the schedule making page
                return render(request, 'studentprofile/schedule.html', context)
    else:
        print("no :( -----------------------------")

def edit_profile(request):
    student = Student.objects.get(user=request.user)
    student.edit = True
    student.save()
    return HttpResponseRedirect(reverse('student profile'))

class ProfileView(generic.TemplateView):
    model = Student
    template_name = 'studentprofile.html'

