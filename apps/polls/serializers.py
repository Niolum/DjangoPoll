from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.polls.models import Poll, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']

    @extend_schema_field(AnswerSerializer(many=True))
    def get_answers(self, obj):
        data = AnswerSerializer(Answer.objects.filter(question=obj), many=True).data
        return data


class PollListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['id', 'name']


class PollDetailSerializer(serializers.ModelSerializer):
    first_question = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'name', 'first_question']

    @extend_schema_field(QuestionSerializer)
    def get_first_question(self, obj):
        data = QuestionSerializer(Question.objects.get(poll=obj, parent=None)).data
        return data