from typing import Collection, Iterable
from django.db import models
from django.forms import ValidationError
from apps.enterprise.models import Organization
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Invoice(models.Model):
    
    STATUS_CHOICE = {
        "PD": "Pending",
        "CMP": "Completed",
    }
    
    REVIEW_LEVEL = {
        "LVL0": "Level0",
        "LVL1": "Level1",
        "LVL2": "Level2",
        "LVL3": "Level3",
    }
    id = models.CharField(max_length=32, primary_key=True, unique=True, editable=False)
    _for = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invoices')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    _from = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICE)
    review_stage = models.CharField(max_length=20, choices=REVIEW_LEVEL)
    
    currency = models.CharField(max_length=5)
    subtotal = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Invoice {self.id} - {self.for_.name}"

    def calculate_total(self):
        self.subtotal = sum(item.total for item in self.items.all())
        self.total = self.subtotal * (100-self.discount + self.tax)/100
        return self.total
    
    def clean_fields(self, *args, **kwargs):
        return super().clean_fields(*args, **kwargs)
    
    
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    _type = models.ForeignKey("InvoiceType", on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    
    def clean(self):
        if self.type_ and self.type_.name == 'wages' and  self.quantity != 1:
            raise ValidationError("wage can only be paid once")
        return super().clean()
    
    @property
    def total(self):
        return self.quantity * self.unit_price
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
        
        
class InvoiceType(models.Model):
    name = models.CharField(max_length=20) 
    description = models.CharField(max_length=225, blank=True, null=True) 