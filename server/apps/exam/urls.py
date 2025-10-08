from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ExamViewSet, ExamResult, ExamSubmit


router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')

urlpatterns = [
    path('', include(router.urls)),
    path(
        "exams/<int:exam_id>/student/<int:student_id>/results/",
        ExamResult.as_view(),
        name="exam-student-result",
    ),
    path(
        "exams/<int:exam_id>/student/<int:student_id>/submit/",
        ExamSubmit.as_view(),
        name="exam-student-submit",
    )
]
