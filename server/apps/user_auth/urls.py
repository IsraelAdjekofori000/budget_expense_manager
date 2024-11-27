from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api.view import (
    CreateUserView,
    DetailUserView,
    VerifyRefreshTokenView,
    EditUserView, RetrieveNotificationView, ListNotificationView, RetrieveRequestView, ListRequestView
)

urlpatterns = [
    re_path(r'^register/(?P<user_type>vendor|agent)/$', CreateUserView.as_view(), name='register'),
    path('<uuid:pk>/', DetailUserView.as_view(), name='detail'),
    path('edit-profile/<uuid:pk>/', EditUserView.as_view(), name='edit_profile'),
    path('request/<uuid:pk>/', RetrieveRequestView.as_view(), name='request'),
    path('requests/', ListRequestView.as_view(), name='requests_list'),
    path('notification/<int:pk>/', RetrieveNotificationView.as_view(), name='retrieve_notification'),
    path('notifications/', ListNotificationView.as_view(), name='list_notification'),
    path('verify-token/', VerifyRefreshTokenView.as_view(), name='verify_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]