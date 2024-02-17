from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.polls.serializers import PollListSerializer, PollDetailSerializer, QuestionSerializer
from apps.polls.models import Poll, Answer, UserPoll, Question, UserAnswer


class PollListAPIView(APIView):
    serializer_class = PollListSerializer
    permission_classes = [AllowAny]

    def get(self, request) -> Response:
        queryset = Poll.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PollDetailAPIView(APIView):
    serializer_class = PollDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, poll_id: int) -> Response:
        queryset = Poll.objects.filter(id=poll_id).first()
        if not queryset:
            return Response(
                {'error': 'Poll not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user_poll, created = UserPoll.objects.get_or_create(
            user=self.request.user, poll=queryset)

        if created or user_poll.user_answers.count() == 0:
            question = Question.objects.get(poll=queryset, parent=None)
            serializer = self.serializer_class(queryset, context={'current_question': question})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        last_user_answer = user_poll.user_answers.order_by('-created_at').first()
        question = last_user_answer.answer.next_question
        serializer = self.serializer_class(queryset, context={'current_question': question})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AnswerQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, poll_id: int, answer_id: int) -> Response:
        answer = Answer.objects.filter(id=answer_id).first()
        if not answer:
            return Response(
                {'error': 'Answer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user_poll = UserPoll.objects.filter(user=request.user, poll=poll_id).first()
        if not user_poll:
            return Response(
                {'error': 'UserPoll not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        UserAnswer.objects.create(user=request.user, answer=answer, user_poll=user_poll)

        if answer.next_question:
            serializer = QuestionSerializer(answer.next_question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        user_poll.status = 'OVER'
        user_poll.save()

        return Response(
            {'message': 'Poll is over'},
            status=status.HTTP_200_OK
        )