# DjangoPoll

![Static Badge](https://img.shields.io/badge/python-3.12-blue?style=plastic&logo=python&link=https%3A%2F%2Fwww.python.org%2F)
![Static Badge](https://img.shields.io/badge/django-5.0-%20%23092E20?style=plastic&logo=Django&label=Django&link=https%3A%2F%2Fwww.djangoproject.com%2F)
![Static Badge](https://img.shields.io/badge/DRF-3%2C14-%23ED1C24?style=plastic&link=https%3A%2F%2Fwww.django-rest-framework.org%2F)
![Coverage Status](https://img.shields.io/badge/coverage-97%25-%23f5d442?style=plastic)


## About Project

DjangoPoll is an API for conducting polls. Implemented the ability to register a user, view all polls, the ability to answer questions with the output of the next question depending on the answer to the previous one (Building questions in the form of a tree using the django-mptt library), as well as viewing poll statistics and each question (implemented using pure SQL without Django ORM).


## Features
- **[Python](https://www.python.org/)** (version 3.12)
- **[Django](https://www.djangoproject.com/)** (version 5.0)
- **[DRF](https://www.django-rest-framework.org/)** (version 3.14)
- **[django-mptt](https://github.com/django-mptt/django-mptt)**
- **[PostgreSQL](https://www.postgresql.org/)**
- **[Docker Compose](https://docs.docker.com/compose/)**


## Quickstart

First, clone project

``` 
git clone https://github.com/Niolum/DjangoPoll.git
```

Further, set up the virtual environment and the main dependencies from the ``requirements.txt``

```
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

Then, create .env file. set environment variables and create database.

Example ``.env``:

```
DATABASE_NAME=db_name
DATABASE_USER=username
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432

DEBUG=False
SECRET_KEY='some_secret_key'
```

Before starting, you need to execute several commands:

```
python manage.py migrate
```

Run application:

```
python manage.py runserver
```

Open your web browser and navigate to http://localhost:8000/api/v1/docs/ to access your Swagger.

For start in docker-compose create .env_docker:

```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name

DATABASE_NAME=db_name
DATABASE_USER=username
DATABASE_PASSWORD=password
DATABASE_HOST='db'
DATABASE_PORT=5431

DEBUG=False
SECRET_KEY='some_secret_key'
```

To start the project, use the following command:

```
docker-compose up -d
```

## Run test


To run all the tests of a project, simply run the pytest command:

```
pytest