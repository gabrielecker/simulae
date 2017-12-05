from exams.models import Answer
from rest.serializers import AnswerSerializer
from rest_framework.viewsets import ModelViewSet


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
