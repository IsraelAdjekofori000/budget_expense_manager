
def profile_image_upload_location(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'profile_pic.{ext}'
    return f'{instance.id}/photos/{filename}'


def product_image_upload_location(instance, filename):
    if instance.vendor:
        ext = filename.split('.')[-1]
        filename = f'vendor_img.{ext}'
        return f'{instance.vendor.id}/photos/{filename}'


def get_anonymous_user(user):
    from .models import Stages
    obj, _ = user.objects.get_or_create(
        password='anonymous_user',
        email='anonymous@user.com',
    )
    return obj
