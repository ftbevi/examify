from django.contrib import admin

from apps.student.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass