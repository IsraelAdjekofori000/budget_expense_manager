from rest_framework import serializers
from ..models import Organization, OrganizationEmployee


class OrganizationSerializer(serializers.ModelSerializer):
    #TODO -- test 
        
    class Meta:
        model = Organization
        fields = ['id', 'name', 'email', 'tel_number', 'address', 'image', 'bio']
  
        
class OrganizationEmployeeSerializer(serializers.ModelSerializer):
    #TODO -- test

    class Meta:
        model = OrganizationEmployee
        fields = ['organization', 'user', 'contract_detail', 'is_admin']
        