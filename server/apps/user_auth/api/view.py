from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    ## TESTED 
    
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data)
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
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class DetailUserView(generics.RetrieveAPIView):
    # TESTED
    
    serializer_class = UserSerializer
    queryset = User.objects.all()

    
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