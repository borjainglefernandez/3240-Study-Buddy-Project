from django.apps import AppConfig
from .models import Schedule
import studentprofile

class StudentprofileConfig(AppConfig):
    name = 'studentprofile'
    # def ready(self):
    #     pass
    #     # try:
    #     #     go = Schedule.objects.get(pk=1)
    #     # except Schedule.DoesNotExist or studentprofile.models.DoesNotExist:
    #     #     go = Schedule.objects.create(pk=1)
    #     #     go.save()
