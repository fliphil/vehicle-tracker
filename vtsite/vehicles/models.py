from django.conf import settings
from django.db import models


class Vehicle(models.Model):
    """
    Store vehicle data
    """
    # Unique ID of the vehicle
    plate = models.CharField(max_length=20)
    # Description of the vehicle
    desc = models.CharField(max_length=50)
    # Photo of the vehicle, relative to MEDIA_URL
    photo = models.ImageField(upload_to='photos', default='photos/no-image.jpg')
    # The odometer value of the vehicle
    odometer = models.IntegerField(default=0)

    def __str__(self):
        return str(self.plate) + "-" + str(self.desc)


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
    vehicle_plate = models.CharField(max_length=20,
                                     blank=True,
                                     null=True)
    vehicle_desc = models.CharField(max_length=50,
                                    blank=True,
                                    null=True)
    destination = models.CharField(max_length=200)
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
               str(self.vehicle_plate)


class VehicleStatus(models.Model):
    """
    Track various status items related to a vehicle
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    on_trip = models.BooleanField(default=False)
    most_recent_trip = models.ForeignKey(TripReservation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.vehicle)


class UserStatus(models.Model):
    """
    Track various status items related to a user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    on_trip = models.BooleanField(default=False)
    most_recent_trip = models.ForeignKey(TripReservation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user)
