from datetime import datetime

from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase

from .serializers import L2TokenRefreshSerializer
from ..token import L2RefreshToken


class BaseTokenCookieView(TokenViewBase):
    message = None

    def get_auth_data(self, request):
        pass

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_auth_data(request))

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(self.message, status=HTTP_200_OK)
        if 'access' in serializer.validated_data:
            access_token_expiration = datetime.fromtimestamp(
                AccessToken(serializer.validated_data['access']).payload['exp']
            )

            response.set_cookie(
                key='access_token',
                value=serializer.validated_data['access'],
                expires=access_token_expiration,
                httponly=True,
                secure=True,
                samesite='Strict',
            )

        if 'refresh' in serializer.validated_data:
            response.set_cookie(
                key='refresh_token',
                value=serializer.validated_data['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax',
                path=reverse('token_refresh')
            )

        return response


class LoginView(BaseTokenCookieView):
    """
    Cookie based login view
    """
    serializer_class = TokenObtainPairSerializer
    message = {'message': 'Login successful'}

    def get_auth_data(self, request):
        return request.data


class RefreshTokenView(BaseTokenCookieView):
    message = None
    serializer_class = L2TokenRefreshSerializer  # implements revocation policies

    def get_auth_data(self, request):
        return {'refresh': request.COOKIES.get('refresh_token', None)}


# class VerifyRefreshTokenView(BaseTokenCookieView):
#     message = {'valid': True}
#     serializer_class = TokenVerifySerializer
#
#     def get_auth_data(self, request):
#         return {'token': request.COOKIE.get('refresh_token', None)}


class LogOutView(APIView):
    permission_classes = IsAuthenticated,

    @staticmethod
    def post(request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                refresh_token = L2RefreshToken(refresh_token)
                refresh_token.blacklist()
            except AttributeError:
                raise AttributeError('blacklist app must be installed')

            response = Response({'message': 'Logout Successful'}, status=HTTP_200_OK)
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response
        else:
            return Response({'message': "Refresh token not provided"}, status=HTTP_400_BAD_REQUEST)


