import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Exam, ExamQuestion, Question


class ExamModelTest(TestCase):
    @pytest.mark.django_db
    def test_exam_creation(self):
        exam = Exam.objects.create(name="Test Exam")
        assert exam.name == "Test Exam"
        assert str(exam) == "Test Exam"

    @pytest.mark.django_db
    def test_exam_with_questions(self):
        question = Question.objects.create(text="What is 2+2?", options=["3", "4", "5"], correct_alternative=1)
        exam = Exam.objects.create(name="Math Exam")
        exam.questions.add(question)
        assert exam.questions.count() == 1
        assert question.exams.count() == 1

    @pytest.mark.django_db
    def test_exam_with_examquestion(self):
        question = Question.objects.create(text="What is 2+2?", options=["3", "4", "5"], correct_alternative=1)
        exam = Exam.objects.create(name="Math Exam")
        exam_question = ExamQuestion.objects.create(
            exam=exam,
            question=question,
            number=1
        )
        assert exam_question.exam == exam
        assert exam_question.question == question
        assert exam_question.number == 1
        assert str(exam_question) == "Question - Math Exam"

