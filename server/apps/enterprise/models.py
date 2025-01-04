from gettext import translation
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid
from .constant import (ORGANIZATION_TYPE_CHOICES,
                       INDUSTRY_CHOICES,
                       STATUS_CHOICES,
                       )

User = get_user_model()


def profile_image_upload_location(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'brand_image.{ext}'
    return f'enterprise/{instance.organization_name}/brand/{filename}'


class Organization(models.Model):
    # identity 
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    organization_name = models.CharField(_('name of organization/business'), max_length=100, blank=False, null=False,
                                         unique=True)
    organization_type = models.CharField(_('type of organization/business'), max_length=15, blank=False, null=False,
                                         choices=ORGANIZATION_TYPE_CHOICES)
    industry_type = models.CharField(_('type of organization/business'), max_length=30, blank=False, null=False,
                                     choices=INDUSTRY_CHOICES)
    # contacts 
    email = models.EmailField(_("organization Email"), max_length=254)
    tel_number = models.CharField(_("organization Tel number"), max_length=20, blank=True, null=True)
    address = models.CharField(_("Official operational address"), max_length=500, blank=True, null=True)
    image = models.ImageField(_("organization brand logo"), upload_to=profile_image_upload_location, blank=True,
                              null=True)
    # about
    bio = models.TextField(_("organization description"), blank=True, null=True)
    created_at = models.DateField(auto_now=True, editable=False)
    admins = models.ManyToManyField(User, related_name='+')

    # fiscal

    # associates
    associates = models.ManyToManyField(User, through='OrganizationAssociates', related_name='org_at')

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        permissions = [
            ('AD', 'admin permission'),
            ('can_UD', 'can update and delete'),
        ]

    def __str__(self):
        return self.organization_name

    def get_absolute_url(self):
        return reverse("organization", kwargs={"pk": self.pk})

    def get_org(self):
        return self

    def is_employee(self, user):
        return bool(self.employees.filter(user=user))

    def is_vendor(self, vendor):
        return bool(self.vendors.filter(vendor=vendor))


class OrganizationAssociates(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='org_associates')
    associate = models.ForeignKey(User, on_delete=models.CASCADE)  # TODO

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'associate'],
                                    name='unique_OrganizationAssociates_organization_associate')
        ]

    def __str__(self):
        return f"{self.associate.username} @ {self.organization.organization_name}"


class AssociateDetail(models.Model):
    associate = models.OneToOneField(OrganizationAssociates, on_delete=models.CASCADE, related_name='contract_detail')
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(_("Active Status"), default=True)
    start_date = models.DateField(_("Start Date"), auto_now_add=True)
    description = models.TextField(_("Notes"), null=True, blank=True)

    # wage_info =
    # payment_info =

    def __str__(self) -> str:
        if hasattr(self, 'associate'):
            return f'{self.associate}'
        return 'empty'

    def save(self, *args, **kwargs):
        self.clean()  # Ensure custom validation logic is executed
        super().save(*args, **kwargs)


class Category(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    supervisor = models.ForeignKey(User, related_name='supervisor_of', on_delete=models.PROTECT)

    # budget_statement =

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        constraints = [
            models.UniqueConstraint(fields=['organization', 'name'],
                                    name='unique_Category_organization_name')
        ]

    def __str__(self):
        return self.name

    def get_org(self):
        return self.organization


class OrganizationAssociateRequest(models.Model):
    organization = models.ForeignKey(Organization, related_name='_requests',
                                     help_text=_("The organization this vendor supplies to."), on_delete=models.CASCADE)
    associate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='associate_request')

    created_at = models.DateTimeField(auto_now=True, editable=False)
    request_status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    message = models.CharField(max_length=500)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('organization', 'associate'),
                                    name='unique_OrganizationAssociateRequest_organization_associate')
        ]

    def get_org(self):
        """called to check user permission over this request"""
        return self.organization


