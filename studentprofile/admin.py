from django.contrib import admin
from .models import Student, Schedule, Class


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'year', 'groupme_id')

admin.site.register(Schedule)