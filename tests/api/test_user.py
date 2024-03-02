import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = {
        'email': 'test@mail.ru',
        'username': 'test',
        'password': 'test_password',
        'password2': 'test_password'
    }

    response = client.post('/api/v1/account/register/', payload)

    assert response.status_code == 201
    assert response.data['response'] == 'User has been registered'


@pytest.mark.django_db
def test_login_user(client, user):
    response = client.post('/api/v1/account/login/', dict(username='test', password='test_password'))

    assert response.status_code == 200
    assert response.data['username'] == 'test'
    assert response.data['email'] == 'test@mail.ru'


@pytest.mark.django_db
def test_login_user_fali(client):
    response = client.post('/api/v1/account/login/', dict(username='test', password='test_password'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_get_me(auth_client):
    response = auth_client.get('/api/v1/account/user/', dict(username='test', password='test_password'))

    assert response.status_code == 200
    assert response.data['username'] == 'test'
    assert response.data['email'] == 'test@mail.ru'


@pytest.mark.django_db
def test_logout_user(client, user):
    response = client.post('/api/v1/account/login/', dict(username='test', password='test_password'))

    auth_header = response.data['tokens']['access']
    refresh = response.data['tokens']['refresh']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_header}')

    response = client.post('/api/v1/account/logout/', dict(refresh=refresh))

    assert response.status_code == 205

