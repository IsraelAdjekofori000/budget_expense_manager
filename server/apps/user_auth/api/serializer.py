from rest_framework import serializers
from ..models import User, UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio', 'phone_number']
        
        

class UserSerializer( serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            }
        depth = 1
        


