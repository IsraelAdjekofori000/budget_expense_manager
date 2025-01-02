from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Agent, Vendor, User, Notification


class UserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=40, write_only=True)
    email = serializers.EmailField()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = ['id', 'username', 'last_name', 'first_name', 'profile_image', 'bio', 'phone_number']


class VendorSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='username')
    description = serializers.CharField(source='bio')

    class Meta:
        model = Vendor
        fields = ['id', 'vendor_name', 'last_name', 'first_name', 'email', 'password', 'profile_image', 'description',
                  'phone_number', 'address', 'website', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            }

    def create(self, validated_data):
        return Vendor.objects.create_user(**validated_data)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# --------------------- Notification ------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'header', 'message', 'created_at', 'seen']