from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


def profile_image_upload_location(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'profile_pic.{ext}'
    return f'{instance.id}/photos/{filename}'



class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.EmailField(_('User active email'), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    
    bio = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    profile_image = models.ImageField(_('user media uploads'), upload_to=profile_image_upload_location, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.get_full_name()
        
    def clean(self):
        super().clean()
        # TODO add check for country code  
        
        if not self.bio and not self.phone_number and not self.profile_image:
            raise ValidationError(_('At least one field (bio, phone_number, profile_image) must be filled.'))
    