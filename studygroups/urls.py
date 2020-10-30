from django.contrib import admin
from django.urls import path, include
from . import views

from django.views.generic import TemplateView

app_name = "studygroups"

urlpatterns = [
    path('groups/create/', TemplateView.as_view(template_name = "studygroups/groupCreate.html"), name='newGroup'),
    path('groups/create/make', views.makeGroup, name='generateGroup')
]
