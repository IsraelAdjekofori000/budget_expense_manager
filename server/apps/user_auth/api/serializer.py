from rest_framework import serializers
from ..models import User


class UserSerializer( serializers.ModelSerializer):
    # TESTED
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email', 'password', 'profile_image', 'bio', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            }
        
        


