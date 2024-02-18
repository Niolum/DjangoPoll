from django.urls import path

from apps.polls.views import (
    PollListAPIView,
    PollDetailAPIView,
    AnswerQuestionAPIView,
    PollStatisticAPIView
)


app_name = "polls"


urlpatterns = [
    path('', PollListAPIView.as_view(), name='poll_list'),
    path('<int:poll_id>/', PollDetailAPIView.as_view(), name='poll_detail'),
    path(
        'answer_question/<int:poll_id>/<int:answer_id>/',
        AnswerQuestionAPIView.as_view(),
        name='answer_question'
    ),
    path('poll_statistic/<int:poll_id>/', PollStatisticAPIView.as_view(), name='poll_statistic')
]