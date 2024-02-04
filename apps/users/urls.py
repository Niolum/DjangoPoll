from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from apps.users.views import (
    RegistryUserView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserAPIView
)


app_name = "users"


urlpatterns = [
    path('register/', RegistryUserView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login-user'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout-user'),
    path('user/', UserAPIView.as_view(), name='user-info'),
]