import uuid

from django.db import IntegrityError
from rest_framework import serializers
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from ..models import Agent, Vendor, User, Notification


class UserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=40, write_only=True)
    email = serializers.EmailField()

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise IntegrityError
        else:
            _id = uuid.uuid4()
            cache.set(str(_id), validated_data,  timeout=600)
            return str(_id)


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


class EmailVerificationSerializer(serializers.Serializer):
    verification_id = serializers.CharField()

    def validate(self, attrs):
        if not cache.get(attrs['verification_id']):
            raise ValidationError('Verification ID not valid')
        return attrs

    def create(self, validated_data):
        credential = cache.get(validated_data['verification_id'])
        cache.delete(validated_data['verification_id'])
        return User.objects.create_user(**credential)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# --------------------- Notification ------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'header', 'message', 'created_at', 'seen']