from django.urls import path, include

urlpatterns = [
    path('account/', include('apps.users.urls', namespace='user')),
    path('polls/', include('apps.polls.urls', namespace='poll'))
]