from django.urls import path, re_path
from .api.view import (
    CreateUserView,
    DetailUserView,
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
]