from django.contrib import admin
from django.urls import path, include
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('profile/schedule/', TemplateView.as_view(template_name = "studentprofile/schedule.html"), name='newSchedule'),
    path('profile/schedule/make', views.make, name='generateSchedule')
]
