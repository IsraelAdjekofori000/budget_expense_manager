from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api.view import (
    CreateUserView,
    DetailUserView,
    VerifyRefreshTokenView,
    EditUserView
)



urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('<uuid:pk>/', DetailUserView.as_view(), name='detail'),
    path('edit-profile/', EditUserView.as_view(), name='edit_profile'),
    path('verify-token/', VerifyRefreshTokenView.as_view(), name='verify_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]