from exams.models import Answer
from rest_framework.serializers import HyperlinkedModelSerializer


class AnswerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('exam', 'choice', 'created_date', 'updated_date', 'active')
