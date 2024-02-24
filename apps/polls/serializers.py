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
    current_question = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'name', 'current_question', 'status']

    @extend_schema_field(QuestionSerializer)
    def get_current_question(self, obj):
        question = self.context['current_question']
        if question:
            data = QuestionSerializer(question).data
        else:
            data = None
        return data
    
    @extend_schema_field(str)
    def get_status(self, obj):
        question = self.context['current_question']
        if question:
            data = 'START'
        else:
            data = 'OVER'
        return data


class PollStatisticSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    count_poll_completers = serializers.IntegerField()
    count_poll_non_completers = serializers.IntegerField()


class AnswerStatisticSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()
    count_answer = serializers.IntegerField()


class QuestionStatisticSerializer(serializers.Serializer):
    count_user_poll = serializers.IntegerField()
    statistic = AnswerStatisticSerializer(many=True)
