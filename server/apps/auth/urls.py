from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .api.view import LoginView, LogOutView, RefreshTokenView

urlpatterns = [
    # path('verify-token/', TokenVerifyView.as_view(), name='verify_token'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('refresh-token/', RefreshTokenView.as_view(), name='token_refresh'),
]
