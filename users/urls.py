from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserRegisterAPIView, UserDetailAPIView, UserUpdateAPIView, UserDeleteAPIView

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterAPIView.as_view(), name='register-user'),
    path('detail/<int:pk>/', UserDetailAPIView.as_view(), name='detail-user'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update-user'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='delete-user'),
] + router.urls
