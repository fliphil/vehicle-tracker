from django.conf import settings
from django.db import models


class Vehicle(models.Model):
    """
    Store vehicle data
    """
    # Unique description of the vehicle
    vehicle_desc = models.CharField(max_length=250)

    def __init__(self):
        models.Model.__init(self)

        # Make an entry in the VehicleStatus table
        vehicle_status = VehicleStatus(vehicle=self)
        vehicle_status.save()

    def __str__(self):
        return self.vehicle_desc

    def can_reserve(self):
        """
        Check whether this user is able to reserve a vehicle.
        Only 1 vehicle can be reserved by a user at a time.
        :return: True or False
        """
        # Find the entry for this user
        status = UserStatus.objects.get(user=self)

        if status.on_trip is True:
            return False
        else:
            return True


class TripReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    vehicle = models.ForeignKey(Vehicle)
    odometer = models.IntegerField()
    time_check_out = models.DateTimeField(auto_now_add=True)
    time_check_in = models.DateTimeField()


class VehicleStatus(models.Model):
    """
    Track various status items related to a vehicle
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    on_trip = models.BooleanField(default=False)
    most_recent_trip = models.ForeignKey(TripReservation, null=True)


class UserStatus(models.Model):
    """
    Track various status items related to a user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    on_trip = models.BooleanField(default=False)
    most_recent_trip = models.ForeignKey(TripReservation, null=True)
