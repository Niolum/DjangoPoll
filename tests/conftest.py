import pytest
from rest_framework.test import APIClient

from apps.users.models import User
from apps.polls.models import Poll, Question, Answer


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    payload = {
        'email': 'test@mail.ru',
        'username': 'test',
        'password': 'test_password',
        'password2': 'test_password'
    }

    user = User(
        email=payload['email'],
        username=payload['username'],
    )

    user.set_password(payload['password'])
    user.save()

    return user


@pytest.fixture
def auth_client(client, user):
    response = client.post('/api/v1/account/login/', dict(username='test', password='test_password'))

    auth_header = response.data['tokens']['access']

    client.force_authenticate(user, f'Bearer {auth_header}')

    return client


@pytest.fixture
def poll():
    poll_payload = {
        'name': 'test poll',
        'count_questions': 3
    }

    poll = Poll(
        name=poll_payload['name'],
        count_questions=poll_payload['count_questions']
    )
    poll.save()

    return poll


@pytest.fixture
def questions(poll):
    question_one = Question(
        text='Question 1',
        poll=poll
    )
    question_one.save()

    question_two = Question(
        text='Question 2',
        poll=poll,
        parent=question_one
    )
    question_two.save()

    return question_one, question_two


@pytest.fixture
def answers(poll, questions):
    answer_one_for_question_one = Answer(
        text='Answer 1 for first question',
        question=questions[0]
    )
    answer_one_for_question_one.save()

    answer_two_for_question_one = Answer(
        text='Answer 2 for first question',
        question=questions[0],
        next_question=questions[1]
    )
    answer_two_for_question_one.save()

    answer_one_for_question_two = Answer(
        text='Answer 1 for second question',
        question=questions[1]
    )
    answer_one_for_question_two.save()

    answer_two_for_question_two = Answer(
        text='Answer 2 for secon question',
        question=questions[1]
    )
    answer_two_for_question_two.save()

    return (
        answer_one_for_question_one,
        answer_two_for_question_one,
        answer_one_for_question_two,
        answer_two_for_question_two
    )
