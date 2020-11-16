from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Schedule, Course, Class, Student
from django.contrib.auth.models import User

# Create your views here.
class NewScheduleView(generic.TemplateView):
    #model = Comments
    template_name = 'studentprofile/schedule.html'

def make(request):
    print(request.user)
    # schedule = Schedule.objects.create()
    print(request.POST)
    # Method of identifying which inputs are valid

    # Remake the iterable array for the template
    #
    # This is the same thing we had to do in mysite/views.py for
    # the initial profile creation
    user = User.objects.get(pk=request.user.id)
    numC = [] # We have to reinput num for each error message that may show up
    for i in range(0, user.student.num):
        numC.append(1)

    # General Error for invalid input
    general_error = render(request, 'studentprofile/schedule.html', { # Redirects the user to the schedule page again
        'error_message': "General Error", # Description for the error message displayed
        'numC': numC
    })

    # Error for if class number is not a digit
    class_number_digit_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Class number must be a digit.",
        'numC': numC
    })

    # Error for if class number is not 4 digits
    class_number_length_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Class number must be 4 digits.",
        'numC': numC
    })

    # Error for if class is not formatted correctly
    class_input_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Class must be a course mnemonic (i.e. CS) followed by a space followed by a 4 digit number (i.e. 3240).",
        'numC': numC
    })

    # Error for if strength is not a digit
    strength_digit_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Strength must be a digit.",
        'numC': numC
    })

    # Error for if strength is not a digit between 1 and 5
    strenth_range_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Strength must be a digit between 1 and 5.",
        'numC': numC
    })

    # Error for if a course inputted does not exist
    course_does_not_exist_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "One or more courses inputted does not exist.",
        'numC': numC
    })

    # Error for if there are not enough classes inputted
    not_enough_classes_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "You are missing some required course fields.",
        'numC': numC
    })

    # Error for if there are not enough strengths inputted
    not_enough_strengths_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "You are missing some required strength fields.",
        'numC': numC
    })

    # Error for inputting a class multiple times
    multiple_entries_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "One or more classes entered multiple times. Each course field should be unique.",
        'numC': numC
    })
    
    # Error for null schedule in Student Object
    null_schedule_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Enter in one or more classes to complete your schedule.",
        'numC': numC
    })
    
    classKeys = sorted([key for key in request.POST.keys() if ("class" in key)])
    strengthKeys = sorted([key for key in request.POST.keys() if ("strength" in key)])

    print(classKeys, strengthKeys)
    good = True
    courses = []
    strengths = []
    for i in range(len(classKeys)):
        good = True

        # If one or more strengths inputted are not in the 1-5 range, raise an error
        if request.POST[strengthKeys[i]].isdigit():
            if not (1 <= int(request.POST[strengthKeys[i]]) <= 5):
                print(request.POST[strengthKeys[i]], "is not in range")
                good = False
                return strenth_range_error

        # If no class or strength is entered, raise an error
        elif request.POST[strengthKeys[i]] == '' and request.POST[classKeys[i]] == '':
            return null_schedule_error
        
        # If one or more strengths inputted are blank, raise an error
        elif request.POST[strengthKeys[i]] == '':
            return not_enough_strengths_error

        # If one or more strengths inputted are not digits, raise an error
        else:
            print(request.POST[strengthKeys[i]], "is not a digit")
            good = False
            return strength_digit_error

        if not good:
            return general_error

        parts = request.POST[classKeys[i]].strip().split(" ")
        if len(parts) == 2:
            mn = parts[0]
            num = parts[1]

            # If the number inputted for the class is not 4 digits, raise an error
            if len(num) != 4:
                print(num, "is not a correct length")
                good = False
                return class_number_length_error

            # If the number inputted for the class is not a digit, raise an error
            elif not num.isdigit():
                print(num, "is not a digit")
                good = False
                return class_number_digit_error

            else:
                try:
                    go = Course.objects.get(mnemonic=mn, number=int(num))
                    courses.append(go)
                    strengths.append(int(request.POST[strengthKeys[i]]))

                # If the inputted course is in a valid format but does not exist, raise an error
                except Course.DoesNotExist:
                    print("Failed to find", mn, num)
                    good = False
                    return course_does_not_exist_error

        # If one or more class field is blank, raise an error
        elif request.POST[classKeys[i]] == '':
            return not_enough_classes_error

        # If class is not formatted correctly, raise an error
        else:
            print(request.POST[classKeys[i]], "did not split well")
            good = False
            return class_input_error

    print(len(courses), len(strengths), good)

    if len(courses) > 0:
        sched = Schedule.objects.create()
        for i in range(len(courses)):
            c = Class(course=courses[i], schedule=sched, strength=strengths[i])
            c.save()
        sched.save()
        student = Student.objects.get(user=request.user)
        print(student.name)
        try:
            student.schedule = sched
            print(sched.get_classes())
        # raises an error if multiple entries for same class
        except Class.MultipleObjectsReturned:
            print("Multiple same class entries")
            return multiple_entries_error
        student.save()

    return HttpResponseRedirect(reverse('student profile'))