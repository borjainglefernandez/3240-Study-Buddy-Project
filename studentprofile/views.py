from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Schedule, Course, Class, Student

# Create your views here.
class NewScheduleView(generic.TemplateView):
    #model = Comments
    template_name = 'studentprofile/schedule.html'

def make(request):
    print(request.user)
    # schedule = Schedule.objects.create()
    print(request.POST)
    # Method of identifying which inputs are valid

    # General Error for invalid input
    general_error = render(request, 'studentprofile/schedule.html', { # Redirects the user to the schedule page again
        'error_message': "General Error", # Description for the error message displayed
    })

    # Error for if class number is not a digit
    class_number_digit_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Class number must be a digit",
    })

    # Error for if class number is not 4 digits
    class_number_length_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Class number must be 4 digits",
    })

    # Error for if class is not formatted correctly
    class_input_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Class must be a course mnemonic (i.e. CS) followed by a space followed by a 4 digit number (i.e. 3240)",
    })

    # Error for if strength is not a digit
    strength_digit_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Strength must be a digit",
    })

    # Error for if strength is not a digit between 1 and 5
    strenth_range_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "Strength must be a digit between 1 and 5",
    })

    # Error for if a course inputted does not exist
    course_does_not_exist_error = render(request, 'studentprofile/schedule.html', {
        'error_message': "One or more courses inputted does not exist",
    })

    classKeys = sorted([key for key in request.POST.keys() if ("class" in key)])
    strengthKeys = sorted([key for key in request.POST.keys() if ("strength" in key)])

    print(classKeys, strengthKeys)
    good = True
    courses = []
    strengths = []
    for i in range(len(classKeys)):
        good = True
        # print(i)
        if request.POST[strengthKeys[i]].isdigit():
            if not (1 <= int(request.POST[strengthKeys[i]]) <= 5):
                print(request.POST[strengthKeys[i]], "is not in range")
                good = False
                return strenth_range_error
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
            if len(num) != 4:
                print(num, "is not a correct length")
                good = False
                return class_number_length_error

            elif not num.isdigit():
                print(num, "is not a digit")
                good = False
                return class_number_digit_error

            else:
                try:
                    go = Course.objects.get(mnemonic=mn, number=int(num))
                    courses.append(go)
                    strengths.append(int(request.POST[strengthKeys[i]]))
                except Course.DoesNotExist:
                    print("Failed to find", mn, num)
                    good = False
                    return course_does_not_exist_error
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
        student.schedule = sched
        student.save()

    return HttpResponseRedirect(reverse('student profile'))