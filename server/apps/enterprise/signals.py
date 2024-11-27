from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import OrganizationAssociateRequest
from ..user_auth.models import Notification


@receiver(post_delete, sender=OrganizationAssociateRequest)
def send_notification(sender, instance, *args, **kwargs):
    if instance.request_status == 'APPR':
        notification = {
            'user': instance.associate,
            'header': 'Join Request Approved',
            'message': f'Your request to join {instance.organization.organization_name} as a {instance.associate.__class__.__name__}'
                       f'has been approved'
        }
        Notification.objects.create(**notification)
    else:
        # Assumes instance.request_status == 'REJT'
        notification = {
            'user': instance.associate,
            'header': 'Join Request Rejected',
            'message': f'Your request to join {instance.organization.organization_name} as a {instance.associate.__class__.__name__}'
                       f'has been rejected'
        }
        Notification.objects.create(**notification)

