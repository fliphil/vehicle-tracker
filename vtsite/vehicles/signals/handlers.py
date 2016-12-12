from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Vehicle
from ..models import VehicleStatus
from ..models import UserStatus


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='create_user_status')
def create_user_status(sender, instance, created, **kwargs):
    if created is True:
        UserStatus.objects.create(user=instance)


@receiver(post_save, sender=Vehicle, dispatch_uid='create_vehicle_status')
def create_vehicle_status(sender, instance, created, **kwargs):
    if created is True:
        VehicleStatus.objects.create(vehicle=instance)