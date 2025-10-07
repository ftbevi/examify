from django.db import models


class Answer(models.Model):
    student = models.ForeignKey(
        "student.Student",
        related_name='answers',
        on_delete=models.CASCADE
    )
    exam = models.ForeignKey(
        "exam.Exam",
        related_name='answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        "question.Question",
        related_name='answers',
        on_delete=models.CASCADE
    )
    alternative = models.ForeignKey(
        "question.Alternative",
        related_name='answers',
        on_delete=models.CASCADE
    )
    
    justify_alternative = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (
            'student', 'exam', 'question', 'alternative'
        )

    def __str__(self):
        return f"{self.justify_alternative or self.id}"
