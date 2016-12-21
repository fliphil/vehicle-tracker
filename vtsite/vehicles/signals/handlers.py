from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Vehicle
from ..models import VehicleStatus
from ..models import UserStatus
from ..models import TripReservation


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='create_user_status')
def create_user_status(sender, instance, created, **kwargs):
    if created is True:
        UserStatus.objects.create(user=instance)


@receiver(post_save, sender=Vehicle, dispatch_uid='create_vehicle_status')
def create_vehicle_status(sender, instance, created, **kwargs):
    if created is True:
        VehicleStatus.objects.create(vehicle=instance)


@receiver(post_save, sender=TripReservation, dispatch_uid='init_trip_reserve')
def init_trip_reserve(sender, instance, created, **kwargs):
    if created is True:
        # Copy some important user/vehicle info for future reference
        user = instance.user
        vehicle = instance.vehicle

        instance.user_first_name = user.first_name
        instance.user_last_name = user.last_name
        instance.vehicle_desc = vehicle.vehicle_desc

        # Not an infinite loop because this signal requires 'created'
        instance.save()