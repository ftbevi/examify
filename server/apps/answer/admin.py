from django.contrib import admin

from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass