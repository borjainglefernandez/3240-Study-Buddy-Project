from django.contrib import admin

from .models import Course
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('idNumber', 'mnemonic', 'number', 'title')