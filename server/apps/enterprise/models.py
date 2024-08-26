from gettext import translation
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.vendor.models import SeriveCatalogue, ProductCatalogue, BaseOffering, Vendor
import uuid


User = get_user_model()


def profile_image_upload_location(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'brand_image.{ext}'
    return f'enterprise/{instance.name}/brand/{filename}'


class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, unique=True, editable=False)
    name = models.CharField(_('name of organization/business/organisation'), max_length=100, blank=False, null=False, unique=True)
    email = models.EmailField(_("organization Email"), max_length=254)
    tel_number = models.CharField(_("organization Tel number"), max_length=20, blank=True, null=True)
    address = models.CharField(_("Official operational address"), max_length=500, blank=True, null=True)
    image = models.ImageField(_("organization brand logo"), upload_to=profile_image_upload_location, blank=True, null=True)
    bio = models.TextField(_("organization description"), blank=True, null=True)
    
    
    # fiscal

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        permissions = [
            ("can_add_admin_to_organization", "Can add admin"),
            ("can_add_employee_to_organization", "can and employee to organization"),
            ("can_add_department_to_organization", "can add department to organization"),
            ("can_add_vendor_to_organization", "Can add vendor to organization"),
            ("can_view_admin_to_organization", "Can view admin"),
            ("can_view_employees_to_organization", "Can view employees"),
            ("can_view_departments_to_organization", "Can view departments"),
            ("can_view_vendors_to_organization", "Can view vendors"),
            ("can_edit_vendor_to_organization", "Can edit vendor"),
            ("can_delete_vendor_to_organization", "Can delete vendor"),
            ("can_make_payment_request_to_organization", "can and payment request to organization"),
        ]
        
        

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
    def is_admin(self, user):
        try:
            return self.employees.get(user=user).is_admin
        except self.DoesNotExist:
            return False
             
    def is_employee(self, user):
        return bool(self.employees.filter(user=user))
    
    def is_vendor(self, vendor):
        return bool(self.vendors.filter(vendor=vendor))
    
    def add_employee(self, user, contract_detail):
        return OrganizationEmployee.objects.create(organization=self, user=user, contract_detail=contract_detail)
    
    def add_vendor(self, vendor, offering, offering_type, last_offering=None):
        if offering_type == "service":
            content_type = ContentType.objects.get_for_model(SeriveCatalogue)
        elif offering_type == "product":
            content_type = ContentType.objects.get_for_model(ProductCatalogue)
        
        org_vendor = OrganizationVendor(organization=self, vendor=vendor, content_type=content_type, object_id=offering.pk, last_offering=last_offering)
        org_vendor.save()
        return org_vendor     
            
    def add_department(self, name, description, **kwargs):
        dp = Department(organization=self, name=name, description=description)
        dp.save()
        hods = kwargs.get('hods')
        
        if isinstance(hods, (list, tuple)):
            lst_hods = []
            for employee in hods:  
                dp_hod = DepartmentHOD(department=dp, organization_employee=employee)
                dp_hod.full_clean()
                lst_hods.append(dp_hod)
            DepartmentHOD.objects.bulk_create(lst_hods)
            dp.update_employee_count(len(lst_hods))
        elif isinstance(hods, OrganizationEmployee):
            dp_hod = DepartmentHOD(department=dp, organization_employee=employee)
            dp_hod.save()     
            dp.update_employee_count()
            
        return dp    
    
    
class OrganizationEmployee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employed_at') #TODO
    contract_detail = models.ForeignKey('EmploymentDetail', on_delete=models.PROTECT, related_name='employee')
    is_admin = models.BooleanField(default=False) # TODO check if security issue exist if view is bypassed 

    class Meta:
        unique_together = ('organization', 'user')

    def __str__(self):
        return f"{self.user.username} @ {self.organization.name}"
    
    
class EmploymentDetail(models.Model):
    department = models.ForeignKey('Department', on_delete=models.SET_DEFAULT, default=None)  # default would be changed to a generic department 
    role = models.CharField(max_length=100)
    employment_type = models.CharField(_("Employment Type"), max_length=100, help_text=_("The employment type. E.g full-time worker or part-time worker"))
    is_active = models.BooleanField(_("Active Status"), default=True, help_text=_("Currently actively employed or on paid leave"))
    start_date = models.DateField(_("Start Date"), auto_now_add=True)
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    supervisor = models.ForeignKey('OrganizationEmployee', on_delete=models.SET_NULL, blank=True, null=True, related_name='supervised_employees', help_text=_("A reference to the employee's supervisor or manager.")) # default to head of department 
    work_location = models.CharField(_("Work Location"), max_length=255, null=True, blank=True)
    work_hours = models.CharField(_("Work Hours"), max_length=50, null=True, blank=True)
    contract_type = models.CharField(_("Contract Type"), max_length=100, help_text=_("To specify the type of contract (e.g., permanent, temporary, freelance)."))
    performance_review_date = models.DateField(_("Performance Review Date"), null=True, blank=True, help_text=_(" Date of the last performance review"))
    notes = models.TextField(_("Notes"), null=True, blank=True, help_text=_("Additional notes or comments about the employee's employment."))
    # wage_info = 
    # payment_info =
    
    def __str__(self) -> str:
        if hasattr(self, 'employee'):
            return self.employee
        return 'empty'

class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments', help_text=_("organisation this department belong"))
    name = models.CharField(_('Department Name'), max_length=100)
    description = models.TextField(_("Department description"))
    hods = models.ManyToManyField('OrganizationEmployee', through='DepartmentHOD', help_text=_("Head of department"), related_name='hod_of')
    number_of_employee = models.IntegerField(_("Number of employees"))
    # budget_statement = 
    
    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        permissions = [
            ("can_add_employee", "Can add employee"),
            ("can_remove_employee", "Can remove employee"),
            ("can_view_budget", "Can view budget"),
            ("can_edit_description", "Can edit budget")
            
        ]
    
    def __str__(self):
        return self.name
    
    def update_employee_count(self, num=1):
        with translation.atomic():
            self.number_of_employee = F('number_of_employee') + num
            self.save(update_fields=['number_of_employee'])
            self.refresh_from_db()
    
    
class DepartmentHOD(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    organization_employee = models.ForeignKey('OrganizationEmployee', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('department', 'organization_employee'),)
        
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.department and self.department.organization != getattr(self.organization_employee, 'organization', default=None):
            raise ValidationError(_(f"Head of department must be an employee of {self.department.organization}")) 
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        
class OrganizationVendor(BaseOffering):
    organization = models.ForeignKey('Organization', related_name='vendors', help_text=_("The organization this vendor supplies to."), on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    offering_type = models.CharField(_("Offering of offering"), max_length=20)
    last_offering = models.DateField(blank=True, null=True) # TODO logic to update last offering 
    
    # payment_info = 