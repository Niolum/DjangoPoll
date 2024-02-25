import pytest


@pytest.mark.django_db
def test_get_polls(client, poll):
    response = client.get('/api/v1/polls/')

    assert response.status_code == 200
    assert response.data[0]['id'] == 1
    assert response.data[0]['name'] == poll.name


@pytest.mark.django_db
def test_get_poll_detail(auth_client, poll, questions, answers):
    response = auth_client.get(f'/api/v1/polls/{poll.id}/')

    assert response.status_code == 200

    data = response.data
    assert data['id'] == poll.id
    assert data['name'] == poll.name
    assert data['status'] == 'START'
    assert data['current_question']['id'] == questions[0].id
    assert data['current_question']['text'] == questions[0].text
    assert data['current_question']['answers'][0]['id'] == answers[0].id
    assert data['current_question']['answers'][1]['id'] == answers[1].id
    assert data['current_question']['answers'][0]['text'] == answers[0].text
    assert data['current_question']['answers'][1]['text'] == answers[1].text


@pytest.mark.django_db
def test_get_poll_detail_fail(auth_client):
    response = auth_client.get(f'/api/v1/polls/1/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_answer_question(auth_client, poll, answers):
    auth_client.get(f'/api/v1/polls/{poll.id}/')
    response = auth_client.post(f'/api/v1/polls/answer_question/{poll.id}/{answers[0].id}/')

    assert response.status_code == 200
    assert response.data['message'] == 'Poll is over'


@pytest.mark.django_db
def test_answer_question_another_branch(auth_client, poll, questions, answers):
    auth_client.get(f'/api/v1/polls/{poll.id}/')
    response = auth_client.post(f'/api/v1/polls/answer_question/{poll.id}/{answers[1].id}/')

    assert response.status_code == 200

    data = response.data

    assert data['id'] == questions[1].id
    assert data['text'] == questions[1].text
    assert data['answers'][0]['id'] == answers[2].id
    assert data['answers'][1]['id'] == answers[3].id
    assert data['answers'][0]['text'] == answers[2].text
    assert data['answers'][1]['text'] == answers[3].text


@pytest.mark.django_db
def test_answer_question_userpoll_not_found(auth_client, poll, answers):
    response = auth_client.post(f'/api/v1/polls/answer_question/{poll.id}/{answers[1].id}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_answer_question_answer_not_found(auth_client, poll):
    response = auth_client.post(f'/api/v1/polls/answer_question/{poll.id}/1/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_answer_question_poll_not_found(auth_client):
    response = auth_client.post(f'/api/v1/polls/answer_question/1/1/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_poll_statistic(auth_client, poll, questions):
    auth_client.get(f'/api/v1/polls/{poll.id}/')
    response = auth_client.get(f'/api/v1/polls/poll_statistic/{poll.id}/')

    assert response.status_code == 200
    assert response.data['total'] == 1
    assert response.data['count_poll_completers'] == 0
    assert response.data['count_poll_non_completers'] == 1


@pytest.mark.django_db
def test_poll_statistic_failed(auth_client):
    response = auth_client.get(f'/api/v1/polls/poll_statistic/1/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_question_statistic(auth_client, poll, questions, answers):
    auth_client.get(f'/api/v1/polls/{poll.id}/')
    auth_client.post(f'/api/v1/polls/answer_question/{poll.id}/{answers[0].id}/')

    response = auth_client.get(f'/api/v1/polls/question_statistic/{questions[0].id}/')

    assert response.status_code == 200

    data = response.data
    assert data['count_user_poll'] == 1
    assert data['statistic'][0]['answer_id'] == answers[0].id
    assert data['statistic'][0]['count_answer'] == 1
    assert data['statistic'][1]['answer_id'] == answers[1].id
    assert data['statistic'][1]['count_answer'] == 0


@pytest.mark.django_db
def test_question_statistic_failed(auth_client):
    response = auth_client.get(f'/api/v1/polls/question_statistic/1/')

    assert response.status_code == 404



