from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.polls.serializers import (
    PollListSerializer,
    PollDetailSerializer,
    QuestionSerializer,
    PollStatisticSerializer,
    QuestionStatisticSerializer
)
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


class PollStatisticAPIView(APIView):
    serializer_class = PollStatisticSerializer

    def get(self, request, poll_id: int) -> Response:
        if not Poll.objects.filter(id=poll_id).exists():
            return Response(
                {'error': 'Poll not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        with connection.cursor() as cursor:
            status_over = 'OVER'
            status_start = 'START'
            query = f'''SELECT COUNT(id) AS COUNT,
                        (SELECT COUNT(status)
                            FROM polls_userpoll
                            WHERE poll_id = {poll_id} AND status LIKE '{status_over}') AS over,
                        (SELECT COUNT(status)
                            FROM polls_userpoll
                            WHERE poll_id = {poll_id} AND status LIKE '{status_start}') AS start
                        FROM polls_userpoll WHERE poll_id = {poll_id}'''

            cursor.execute(query)
            row = cursor.fetchone()
        
        count, over, start = row
        data = {
            'total': count,
            'count_poll_completers': over,
            'count_poll_non_completers': start
        }
        serializer = self.serializer_class(data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionStatisticAPIView(APIView):
    serializer_class = QuestionStatisticSerializer

    def get(self, request, question_id: int) -> Response:
        if not Question.objects.filter(id=question_id).exists():
            return Response(
                {'error': 'Question not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        count_user_poll = None
        with connection.cursor() as cursor:
            query = f'''SELECT COUNT(id)
                            FROM polls_userpoll
                            WHERE poll_id = 
                                (SELECT poll_id
                                    FROM polls_question
                                    WHERE id = {question_id})'''
            
            cursor.execute(query)
            row = cursor.fetchone()
            count_user_poll = row[0]

            query = f'''SELECT COUNT(answer_id), polls_answer.id FROM polls_useranswer AS user_answer
                            RIGHT OUTER JOIN polls_answer ON (user_answer.answer_id = polls_answer.id)
                            WHERE polls_answer.question_id={question_id}
                            GROUP BY polls_answer.id'''
            cursor.execute(query)
            row = cursor.fetchall()
            print(row)

        data = {
            'count_user_poll': count_user_poll,
            'statistic': []
        }

        for result in row:
            statistic = {
                'answer_id': result[1],
                'count_answer': result[0]
            }
            data['statistic'].append(statistic)

        serializer = self.serializer_class(data)

        return Response(serializer.data, status=status.HTTP_200_OK)
