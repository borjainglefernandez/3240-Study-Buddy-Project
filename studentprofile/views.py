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
        else:
            print(request.POST[strengthKeys[i]], "is not a digit")
            good = False
        if not good:
            continue

        parts = request.POST[classKeys[i]].strip().split(" ")
        if len(parts) == 2:
            mn = parts[0]
            num = parts[1]
            if len(num) != 4:
                print(num, "is not a correct length")
                good = False
            elif not num.isdigit():
                print(num, "is not a digit")
                good = False
            else:
                try:
                    go = Course.objects.get(mnemonic=mn, number=int(num))
                    courses.append(go)
                    strengths.append(int(request.POST[strengthKeys[i]]))
                except Course.DoesNotExist:
                    print("Failed to find", mn, num)
                    good = False
        else:
            print(request.POST[classKeys[i]], "did not split well")
            good = False

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

    # question = get_object_or_404(Question, pk=question_id)
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    return HttpResponseRedirect(reverse('student profile'))