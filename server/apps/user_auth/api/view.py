from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .serializer import AgentSerializer, VendorSerializer, NotificationSerializer, UserSerializer, EmailVerificationSerializer
from ..models import Agent, Notification
from ...enterprise.api.serializer import AssociateRequestSerializer
from ...enterprise.models import OrganizationAssociateRequest
from ...enterprise.permission import IsOwner

User = get_user_model()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# --------------------- USER ------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class CreateUserTypeView(generics.CreateAPIView):
    permission_classes = IsAuthenticated,

    def get_serializer_class(self):
        if self.kwargs.get('user_type') == 'Agent':
            return  AgentSerializer
        return VendorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=HTTP_200_OK)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            _id = serializer.save()
            ver_link = "http://localhost:3000/verify-email/" + f'?id={_id}'
            send_mail("Validate Your Email Address",
                      f'Verify your email here: {ver_link}',
                      'testnoreply@gmail.com',
                      [serializer.validated_data['email']],
                      fail_silently=False
                      )

            return Response({"message": 'Verify email'}, status=HTTP_201_CREATED)
        except IntegrityError:
            raise ValidationError('Email has been used')


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


class VerifyUserEmailView(APIView):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        print(request.COOKIES.get('access_token'))
        verification_id = request.query_params.get('id')

        if verification_id:
            serializer = EmailVerificationSerializer(data={'verification_id': verification_id})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            response = Response(f'{user.email} successfully verified', status=HTTP_200_OK)
            refresh = RefreshToken.for_user(user)
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                path=reverse('token_refresh')
            )

            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                expires=datetime.fromtimestamp(refresh.access_token.payload['exp']),
                httponly=True,
                secure=True,
                samesite='Strict',
            )

            return response


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


