from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel, PolymorphicManager
from django.utils.translation import gettext_lazy as _
import uuid
from .utils import profile_image_upload_location, product_image_upload_location


class AppUserManager(UserManager, PolymorphicManager):
    pass


class User(AbstractUser, PolymorphicModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.EmailField(_('User active email'), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    username = models.CharField(max_length=100, blank=True, unique=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    profile_image = models.ImageField(_('user media uploads'), upload_to=profile_image_upload_location, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = AppUserManager()
    
    def __str__(self):
        return self.get_full_name()
        
    def clean(self):
        super().clean()
        # TODO add check for country code  
        
        if not self.bio and not self.phone_number and not self.profile_image:
            raise ValidationError(_('At least one field (bio, phone_number, profile_image) must be filled.'))

   
class Agent(User):
    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")


class Vendor(User):
    """
    Vendor/Supplier for a particular organization.
    """

    address = models.TextField(_("Address"), blank=True, null=True, help_text=_("Physical address of the vendor."))
    website = models.URLField(_("Website"), blank=True, null=True, help_text=_("Website of the vendor."))
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True,
                                      help_text=_("The date and time when this vendor record was last updated."))

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        permissions = [
            # ("can_add_offering_to_vendor", "Can add offerings to vendor"),
        ]

    def __str__(self):
        return self.username

    @property
    def offerings(self):
        return getattr(self, 'offerings')


class VendorOffering(models.Model):
    OFFERING_CHOICES = (
        ('SERV', 'Service'),
        ('PROD', 'Product'),
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=product_image_upload_location, blank=True, null=True)
    offering_type = models.CharField(max_length=10, choices=OFFERING_CHOICES)
    vendor = models.ForeignKey(Vendor, related_name='offerings', on_delete=models.CASCADE)
    description = models.TimeField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    per = models.CharField(max_length=50)


class Stages(models.Model):
    stage = models.IntegerField()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    header = models.CharField(max_length=100, blank=False) 
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)