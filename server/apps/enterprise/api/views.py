
from uuid import UUID
from django.http import QueryDict
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from guardian.shortcuts import assign_perm
from base.utils import value_or_default

from .serializer import (OrganizationSerializer,
                         OrganizationAdminSerializer, DepartmentSerializer,
                         AssociateRequestSerializer, OrganizationAssociateSerializer,
                         )
from ..permission import IsAdmin, IsOwner
from ..models import Organization, OrganizationAssociateRequest, Department


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ------------------------- ORGANIZATION CRUD  --------------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# C
class CreateOrganizationView(generics.CreateAPIView):
    serializer_class = OrganizationAdminSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def set_permissions(user, org):
        permissions = 'AD',

        for perm in permissions:
            assign_perm(perm, user, org)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.dict() if isinstance(request.data, QueryDict) else request.data
        data['associates'] = [{
            'associate': user.pk,
            'contract_detail': None
        }]
        data['admins'] = [user.pk]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        self.set_permissions(user, org)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# R
class RetrieveOrganizationView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        obj = self.get_object()
        if user in obj.admins.all():
            return OrganizationAdminSerializer
        else:
            return OrganizationSerializer


# U
class UpdateOrganizationView(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = OrganizationAdminSerializer


# D
class DestroyOrganisationView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Organization.objects.all()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -------------- ORGANIZATION ASSOCIATE REQUEST CRUD  -------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class CreateAssociateRequestView(generics.CreateAPIView):
    serializer_class = AssociateRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            'organization': kwargs.get('organization_id'),
            'associate': request.user.id,
            'request_status': 'PEND',
            'message': request.data.get('message', ''),
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveAssociateRequestView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AssociateRequestSerializer

    def get_queryset(self):
        return OrganizationAssociateRequest.objects.filter(organization__pk=self.kwargs.pop('organization_id'))


class ListAssociateRequestView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AssociateRequestSerializer

    def get_queryset(self):
        return OrganizationAssociateRequest.objects.filter(organization__pk=self.kwargs.pop('organization_id'))


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ------------------ ORGANIZATION ASSOCIATE CRUD  -----------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class CreateAssociateView(generics.CreateAPIView):
    # Associate can only be created from existing requests to join organization

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = OrganizationAssociateSerializer

    @staticmethod
    def finish_request(request):
        request.request_status = 'APPR'
        request.delete()

    def get_request(self):
        try:
            print(self.kwargs.get('request_id'), self.kwargs.get('organization_id'))
            return OrganizationAssociateRequest.objects.get(
                pk=self.kwargs.get('request_id'), organization__pk=self.kwargs.get('organization_id')
            )
        except OrganizationAssociateRequest.DoesNotExist:
            raise ValidationError('Invalid for non-existing request')

    def get_organization_pk(self):
        try:
            obj = Organization.objects.get(pk=self.kwargs.get('organization_id'))
            self.check_object_permissions(self.request, obj)
            return obj.pk
        except Organization.DoesNotExist:
            raise ValidationError('Invalid for non-existing enterprise')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organization=self.get_organization_pk())
        self.finish_request(self.get_request())

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(data=serializer.data)
        )


class DeleteAssociateRequestView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return OrganizationAssociateRequest.objects.filter(organization__pk=self.kwargs.get('organization_id'))


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ------------------ DEPARTMENT ASSOCIATE CRUD  -----------------------
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=


class CreateDepartmentView(generics.CreateAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_organization(self):
        try:
            obj = Organization.objects.get(pk=self.kwargs.get('organization_id'))
            self.check_object_permissions(self.request, obj)
            return obj
        except Organization.DoesNotExist:
            raise ValidationError('Invalid for non-existing enterprise')

    def create(self, request, *args, **kwargs):
        data = value_or_default(request.data.dict, request.data)[0]
        data['organization'] = self.get_organization().pk
        data['hod'] = value_or_default(UUID, data['hod'], hex=data['hod'])[0]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(data=serializer.data)
            )


class ListDepartmentView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Department.objects.filter(organization__pk=self.kwargs.get('organization_id'))


class RetrieveDepartmentView(generics.RetrieveAPIView):
    queryset = Department
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Department.objects.filter(organization__pk=self.kwargs.get('organization_id'))