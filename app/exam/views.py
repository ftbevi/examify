from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response
from rest_framework import serializers

from answer.serializers import AnswerSerializer
from .models import Exam
from .serializers import ExamSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Listar Exames",
        description=(
            "Lista todos os Exames existentes."
        ),
        responses=ExamSerializer,
    ),
    create=extend_schema(
        summary="Criar Exame",
        description="Cria um novo Exame com os dados informados.",
        responses=ExamSerializer,
    ),
    retrieve=extend_schema(
        summary="Detalhar Exame",
        description="Retorna os dados completos de um Exame específic.",
        responses=ExamSerializer,
    ),
    update=extend_schema(
        summary="Atualizar Exame",
        description="Atualiza todos os campos de um Exame existente.",
        responses=ExamSerializer,
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de Exame",
        description="Atualiza parcialmente os campos de um exame existente.",
        responses=ExamSerializer,
    ),
    destroy=extend_schema(
        summary="Deletar Exame",
        description=(
            "Deleta um Exame especifico."
        ),
        responses=ExamSerializer,
    ),
)
@extend_schema(tags=["Exame"])
class ExamViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retorna o resultado de um exame realizado por um aluno.",
        description=(
            "Retorna o resultado de um exame realizado por um aluno.\n\n"
        ),
        request=AnswerSerializer(many=True)
    )
)
@extend_schema(tags=["Resultado"])
class ExamResult(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, exam_id, student_id):
        from answer.models import Answer
        from question.models import Question
        from answer.serializers import AnswerSerializer

        answers = Answer.objects.filter(exam=exam_id, student=student_id)
        serializer = AnswerSerializer(answers, many=True)

        correct_answers = Answer.objects.filter(exam=exam_id, student=student_id).filter(alternative__is_correct=True).count()
        total_questions = Question.objects.filter(examquestion__exam=exam_id).count()

        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        return Response({
            'answers': serializer.data,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'percentage': round(percentage, 2)
        }, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        summary="Realiza o registro das respostas de um determinado exame.",
        description=(
            "Recebe uma lista de respostas para um exame.\n\n"
            "Campos de uma resposta: \n\n"
            "- *student*: ID do estudante.\n"
            "- *exam*: ID do exame realizado.\n"
            "- *question*: ID da questão que esta sendo respondida.\n"
            "- *alternative*: ID da alternativa selecionada.\n"
            "- *justify_alternative*: Justificativa, não obrigatória, para a alternativa selecionada.\n"
        ),
        request=AnswerSerializer(many=True)
    )
)
@extend_schema(tags=["Submissão de Gabarito"])
class ExamSubmit(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, exam_id, student_id):
        try:
            from answer.serializers import AnswerSerializer

            serializer = AnswerSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as ex:
            return Response({
                'error': 'Dados inválidos',
                'details': ex.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({
                'error': 'Erro inesperado',
                'message': str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
