from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from apps.users.views import (
    RegistryUserView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserAPIView
)


app_name = "users"


urlpatterns = [
    path('register/', RegistryUserView.as_view(), name='register'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserLoginAPIView.as_view(), name='login-user'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout-user'),
    path('user/', UserAPIView.as_view(), name='user-info'),
]