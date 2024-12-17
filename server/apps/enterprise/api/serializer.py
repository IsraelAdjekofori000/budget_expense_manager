from rest_framework import serializers
from ..models import Organization, OrganizationAssociateRequest, OrganizationAssociates, AssociateDetail, Category
from ...user_auth.models import Agent, User, Vendor


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------------------- CUSTOM SERIALIZERS  ---------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class UserOrganisationPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    """
    This field was created for security and consistency between
    users and the organisations the can and cannot associate with
    for specific roles 
    """
    
    def __init__(self, include=False, **kwargs):
        # exclude by default
        super().__init__(**kwargs)
        self.__include = include

    def get_queryset(self):
        organization = self.parent.initial_data.get('organization')
        queryset = super().get_queryset()
        if organization:
            if self.__include:
                return queryset.filter(org_at__pk=organization)
            else:
                return queryset.exclude(org_at__pk=organization)
        return queryset.none()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ------------------------- ORGANIZATION  ------------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class OrganizationSerializer(serializers.ModelSerializer):
    # TODO -- test

    class Meta:
        model = Organization
        fields = [
            'id', 'organization_name', 'organization_type', 'industry_type',

            'email', 'tel_number', 'address', 'image',

            'bio', 'created_at', 'admins', 'associates'
        ]
        read_only_fields = fields


class OrganizationAssociateAdminSerializer(serializers.ModelSerializer):
    contract_detail = serializers.PrimaryKeyRelatedField(queryset=OrganizationAssociates.objects.all(), allow_null=True)

    class Meta:
        model = OrganizationAssociates
        fields = ['associate', 'contract_detail']


class OrganizationAdminSerializer(serializers.ModelSerializer):
    vendor_count = serializers.SerializerMethodField()
    agent_count = serializers.SerializerMethodField()
    admins = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.instance_of(Agent))
    associates = OrganizationAssociateAdminSerializer(many=True, source='org_associates')

    class Meta:
        p_meta = OrganizationSerializer.Meta
        model = Organization
        fields = [
            'id', 'organization_name', 'organization_type', 'industry_type',

            'email', 'tel_number', 'address', 'image',

            'bio', 'created_at', 'admins', 'agent_count', 'vendor_count', 'associates'
        ]

    @staticmethod
    def get_vendor_count(obj):
        return obj.associates.instance_of(Vendor).count()

    @staticmethod
    def get_agent_count(obj):
        return obj.associates.instance_of(User).count()

    def create(self, validated_data):
        org_associates = validated_data.pop('org_associates')
        admins = validated_data.pop('admins')
        org = Organization.objects.create(**validated_data)
        org.admins.set(admins)
        OrganizationAssociates.objects.bulk_create(
            [
                OrganizationAssociates(
                    organization=org,
                    associate=org_associate['associate'],
                    contract_detail=org_associate['contract_detail']
                ) for org_associate in org_associates
            ]
        )

        return org


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -------------------- ORGANIZATION REQUEST  -------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=


class AssociateRequestSerializer(serializers.ModelSerializer):

    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    associate = UserOrganisationPrimaryKeyRelatedField(queryset=User.objects)

    class Meta:
        model = OrganizationAssociateRequest
        fields = ['id', 'organization', 'associate', 'created_at', 'request_status', 'message']


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -------------------- ORGANIZATION ASSOCIATE  -------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class AssociateContractSerializer(serializers.ModelSerializer):
    associate_type = serializers.SerializerMethodField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects)

    class Meta:
        model = AssociateDetail
        fields = [
            'id', 'categories',
            'role', 'associate_type',
            'is_active', 'start_date',
            'description'
        ]

    @staticmethod
    def get_associate_type(obj):
        return obj.associate.associate.__class__.Meta.verbose_name


class OrganizationAssociateSerializer(serializers.ModelSerializer):
    contract_detail = AssociateContractSerializer()

    class Meta:
        model = OrganizationAssociates
        fields = ['associate', 'contract_detail']

    def create(self, validated_data):
        organization_id = validated_data.pop('organization', None)
        contract_detail = validated_data.pop('contract_detail', {})
        if organization_id:
            organization_associate = OrganizationAssociates.objects.create(
                **validated_data, organization_id=organization_id
            )
            if contract_detail:
                contract_detail['associate'] = organization_associate
                AssociateDetail.objects.create(**contract_detail)

            return organization_associate


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------------------- CATEGORY ASSOCIATE ---------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class CategorySerializer(serializers.ModelSerializer):
    supervisor = UserOrganisationPrimaryKeyRelatedField(queryset=User.objects, include=True)  # write_only=True,
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects)

    class Meta:
        model = Category
        fields = [
           'id', 'organization', 'name', 'description', 'supervisor'
        ]
