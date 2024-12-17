from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import AgentSerializer, VendorSerializer, NotificationSerializer
from ..models import Agent, Notification
from ...enterprise.api.serializer import AssociateRequestSerializer
from ...enterprise.models import OrganizationAssociateRequest
from ...enterprise.permission import IsOwner

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    # TESTED

    def get_serializer_class(self):
        if self.kwargs.get('user_type') == 'agent':
            return AgentSerializer
        else:
            return VendorSerializer

    def create(self, request, *args,  **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        response = {
            'user': serializer.data,
            'refresh': str(token),
            'access': str(token.access_token)
        }
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=HTTP_201_CREATED, headers=headers)


class EditUserView(generics.UpdateAPIView):
    
    # TODO -- disable direct change of password 
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if isinstance(self.request.user, Agent):
            return AgentSerializer
        else:
            return VendorSerializer


class DetailUserView(generics.RetrieveAPIView):
    # TESTED
    queryset = User.objects.all()

    def get_serializer_class(self):
        if isinstance(self.get_object(), Agent):
            return AgentSerializer
        else:
            return VendorSerializer


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# --------------------- Notification ------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# R
class RetrieveNotificationView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        obj.seen = True
        obj.save(update_fields=['seen'])
        return obj


class ListNotificationView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# --------------------- Request CRUD ------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class RetrieveRequestView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = AssociateRequestSerializer

    def get_queryset(self):
        return OrganizationAssociateRequest.objects.filter(associate=self.request.user)


class ListRequestView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = AssociateRequestSerializer

    def get_queryset(self):
        return OrganizationAssociateRequest.objects.filter(associate=self.request.user)


