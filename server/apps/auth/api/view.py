from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class VerifyRefreshTokenView(APIView):
    # TESTED
    def post(self, request, *args, **kwargs):
        token = self.request.data.get('refresh')
        if not token:
            return Response({'error': 'refresh token required'}, status=HTTP_400_BAD_REQUEST)

        else:
            try:
                RefreshToken(token)
                return Response({'valid': True}, status= HTTP_200_OK)
            except TokenError:
                return Response({'valid': False}, status= HTTP_401_UNAUTHORIZED)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        user_jwts = OutstandingToken.objects.filter(user_id=request.user.pk)
        BlacklistedToken.objects.bulk_create(
            [BlacklistedToken(token=token) for token in user_jwts], ignore_conflicts=True
        )
        print(f'{len(user_jwts)} session of {request.user} manually terminal by user')
        return Response(f'successfully logged out of {len(user_jwts)} devices', status=HTTP_200_OK)
