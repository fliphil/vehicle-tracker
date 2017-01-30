from django.conf import settings
from django.db import models


class Vehicle(models.Model):
    """
    Store vehicle data
    """
    # Unique description of the vehicle
    desc = models.CharField(max_length=50)
    # photo = models.ImageField(default='')

    def __str__(self):
        return str(self.desc)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    user_first_name = models.CharField(max_length=30,
                                       blank=True,
                                       null=True)
    user_last_name = models.CharField(max_length=30,
                                      blank=True,
                                      null=True)
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True)
    vehicle_desc = models.CharField(max_length=50,
                                    blank=True,
                                    null=True)
    destination = models.CharField(max_length=100)
    pre_odometer = models.IntegerField()
    pre_fuel_check = models.BooleanField(default=False)
    pre_tire_check = models.BooleanField(default=False)
    pre_damage_check = models.BooleanField(default=False)
    post_odometer = models.IntegerField(null=True, blank=True)
    post_fuel_check = models.BooleanField(default=False)
    post_trash_check = models.BooleanField(default=False)
    post_damage_check = models.BooleanField(default=False)
    post_comments = models.CharField(max_length=500, null=True, blank=True)
    time_check_out = models.DateTimeField(auto_now_add=True)
    time_check_in = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.time_check_out) + '-' +\
               str(self.user_first_name) + '_' + \
               str(self.user_last_name) + '-' + \
               str(self.vehicle_desc)


class VehicleStatus(models.Model):
    """
    Track various status items related to a vehicle
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    on_trip = models.BooleanField(default=False)
    most_recent_trip = models.ForeignKey(TripReservation, null=True, blank=True)

    def __str__(self):
        return str(self.vehicle)


class UserStatus(models.Model):
    """
    Track various status items related to a user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    on_trip = models.BooleanField(default=False)
    most_recent_trip = models.ForeignKey(TripReservation, null=True, blank=True)

    def __str__(self):
        return str(self.user)
