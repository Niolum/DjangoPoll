from django.urls import path, include

urlpatterns = [
    path('account/', include('apps.users.urls', namespace='user')),
]