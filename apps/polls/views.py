from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.polls.serializers import PollListSerializer, PollDetailSerializer, QuestionSerializer
from apps.polls.models import Poll, Answer


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
        
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AnswerQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, answer_id: int) -> Response:
        answer = Answer.objects.filter(id=answer_id).first()
        if not answer:
            return Response(
                {'error': 'Answer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if answer.next_question:
            serializer = QuestionSerializer(answer.next_question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {'message': 'Poll is over'},
            status=status.HTTP_200_OK
        )