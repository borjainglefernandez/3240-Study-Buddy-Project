from django.shortcuts import render
from django.views import generic

# Create your views here.
class NewScheduleView(generic.TemplateView):
    #model = Comments
    template_name = 'studentprofile/schedule.html'

def make(request):
    pass