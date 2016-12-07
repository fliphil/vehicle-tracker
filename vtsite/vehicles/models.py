from django.db import models

class Vehicle(models.Model):
    """
    Store vehicle data
    """
    # Unique description of the vehicle
    vehicle_desc = models.CharField(max_length=250)
    # vehicle_photo = models.ImageField(upload_to=None)

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


class VehicleStatus(models.Model):
    """
    Track various status items related to a vehicle
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    on_trip = models.BooleanField(default=False)


class UserStatus(models.Model):
    """
    Track various status items related to a user
    """
    username = models.CharField(max_length=20, default="")
    on_trip = models.BooleanField(default=False)


class TripReservation(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    odometer = models.IntegerField()
    # date and time of checkout
    # user info for driver who checked out vehicle
    # any other auto populated fields
