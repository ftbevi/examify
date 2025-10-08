from rest_framework import serializers

from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'student', 'exam', 'question', 'alternative', 'justify_alternative']
