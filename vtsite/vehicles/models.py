from django.db import models


class Vehicle(models.Model):
    """
    Store vehicle data
    """
    # Unique description of the vehicle
    vehicle_desc = models.CharField(max_length=250)

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


class User(models.Model):
    """
    Store user data
    """
    # Username for the account
    user_name = models.CharField(max_length=20)
    # Hash digest of the user account password
    user_password_hash = models.CharField(max_length=64)
    # Real-life first name of the user
    user_first_name = models.CharField(max_length=20)
    # Real-life last name of the user
    user_last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.user_first_name + ' ' + self.user_last_name

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
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, default="")
    on_trip = models.BooleanField(default=False)


class TripReservation(models.Model):
    YES_NO = (
            ('Y', 'Yes'),
            ('N', 'No'),
    )
    vehicle = models.ForeignKey(Vehicle)
    user = models.ForeignKey(User)
    #check_out_dt = models.DateField()
    #check_in_dt = models.DateField()
    odometer = models.IntegerField()
    """
    destination = models.CharField(max_length=250)
    comments_check_out = models.CharField(max_length=250)
    comments_check_in = models.CharField(max_length=250)
    tires_inspected = models.CharField(max_length=1, choices=YES_NO)
    damage_check_out = models.CharField(max_length=1, choices=YES_NO)
    damage_check_in = models.CharField(max_length=1, choices=YES_NO)
    fuel_full_check_out = models.CharField(max_length=1, choices=YES_NO)
    fuel_full_check_in = models.CharField(max_length=1, choices=YES_NO)
    vehicle_clean = models.CharField(max_length=1, choices=YES_NO)
    post_accident = models.CharField(max_length=250)
    """
