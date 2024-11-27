from rest_framework import serializers
from ..models import Agent, Vendor, User, Notification


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = ['id', 'username', 'last_name', 'first_name', 'email', 'password', 'profile_image', 'bio',
                  'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            }

    def create(self, validated_data):
        return Agent.objects.create_user(**validated_data)


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