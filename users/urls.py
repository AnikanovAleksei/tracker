from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserCreateAPIView, UserRetrieveAPIView, UserDestroyAPIView, UserUpdateAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('retrieve/<int:pk>/', UserRetrieveAPIView.as_view(), name='retrieve'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update'),
    path('destroy/<int:pk>/', UserDestroyAPIView.as_view(), name='destroy'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
