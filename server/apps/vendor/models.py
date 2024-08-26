from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class Vendor(models.Model):
    """
    Vendor/Supplier for a particular organization.
    """

    name = models.CharField(_("Vendor Name"), max_length=255, help_text=_("Name of the vendor or supplier."))
    offering = models.ManyToManyField("VendorOffering")
    email = models.EmailField(_("Vendor Email"), max_length=254, blank=True, null=True, help_text=_("Email address of the vendor."))
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True, null=True, help_text=_("Contact phone number of the vendor."))
    address = models.TextField(_("Address"), blank=True, null=True, help_text=_("Physical address of the vendor."))
    website = models.URLField(_("Website"), blank=True, null=True, help_text=_("Website of the vendor."))
    description = models.TextField(_("Description"), blank=True, null=True, help_text=_("Description of the vendor's services or products."))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, help_text=_("The date and time when this vendor record was created."))
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True, help_text=_("The date and time when this vendor record was last updated."))

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        permissions = [
            ("can_add_offering_to_vendor", "Can add offerings to vendor"),
        ]
        

    def __str__(self):
        return self.name
    
    def add_offering(self, offering_type, offering, specification=None):
        if offering_type == "service":
            content_type = ContentType.objects.get_for_model(SeriveCatalogue)
        elif offering_type == "product":
            content_type = ContentType.objects.get_for_model(ProductCatalogue)
            
        vendor_off = VendorOffering(content_type=content_type, object_id=offering, specification=specification)
        vendor_off.save()
        return vendor_off        


class BaseOffering(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    offering =  GenericForeignKey('content_type', 'object_id')     # TODO add validation to check that only service and product catalogue are added 

    class Meta:
        abstract = True
    
    def clean_fields(self, *args, **kwargs):     
        catalogues = ContentType.objects.get_for_models(SeriveCatalogue, ProductCatalogue)
        if self.content_type not in (catalogues.get(SeriveCatalogue), catalogues.get(ProductCatalogue)):
            ValidationError(_("must be a service or product"))
        return super().clean_fields(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    
class VendorOffering(BaseOffering):
    specification = models.TextField(help_text=_("information about the particular product or service "), blank=True, null=True)
    

class ProductCatalogue(models.Model):
    name = models.CharField(_("name"), max_length=100, help_text=_("name of product"))
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name 


class SeriveCatalogue(models.Model):
    name = models.CharField(_("name"), max_length=100, help_text=_("name of product"))
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name 