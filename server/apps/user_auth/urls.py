from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api.view import (
    CreateUserView,
    DetailUserView,
    VerifyRefreshTokenView
)



urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('<uuid:pk>/', DetailUserView.as_view(), name='detail'),
    path('verify-token/', VerifyRefreshTokenView.as_view(), name='verify_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]