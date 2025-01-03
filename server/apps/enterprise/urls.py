from django.urls import path
from .api.views import (
    CreateOrganizationView,
    RetrieveOrganizationView,
    UpdateOrganizationView,
    DestroyOrganisationView,
    CreateAssociateRequestView,
    RetrieveAssociateRequestView,
    ListAssociateRequestView,
    DeleteAssociateRequestView,
    CreateAssociateView,
    CreateCategoryView,
    RetrieveCategoryView,
    ListCategoryView
)

urlpatterns = [
    path('create-org/', CreateOrganizationView.as_view(), name='create_org'),
    path('<uuid:pk>/', RetrieveOrganizationView.as_view(), name='detail_org'),
    path('edit-org/<uuid:pk>/', UpdateOrganizationView.as_view(), name='edit_org'),
    path('delete-org/<uuid:pk>/', DestroyOrganisationView.as_view(), name='delete_org'),
    path('<uuid:organization_id>/request-association/', CreateAssociateRequestView.as_view(), name='request_association'),
    path('<uuid:organization_id>/association-request/<int:pk>/', RetrieveAssociateRequestView.as_view(), name='retrieve_request'),
    path('<uuid:organization_id>/association-requests/', ListAssociateRequestView.as_view(), name='list_request'),
    # path('<uuid:organization_id>/update-request/<int:pk>/', UpdateAssociateRequestView.as_view(), name='update_request'),
    path('<uuid:organization_id>/deny-request/<int:pk>/', DeleteAssociateRequestView.as_view(), name='delete_request'),
    path('<uuid:organization_id>/approve-request/<int:request_id>/', CreateAssociateView.as_view(), name='approve-request'),
    path('<uuid:organization_id>/create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('<uuid:organization_id>/categories/', ListCategoryView.as_view(), name='list-categories'),
    path('<uuid:organization_id>/category/<int:pk>', RetrieveCategoryView.as_view(), name='retrieve-category'),
]