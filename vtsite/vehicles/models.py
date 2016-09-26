from django.db import models

# Create your models here.
class Vehicle(models.Model):
    vehicle_desc = models.CharField(max_length=250)
    def __str__(self):
        return self.vehicle_desc

class User(models.Model):
    user_full_name = models.CharField(max_length=50)
    user_password_hash = models.CharField(max_length=64)
    def __str__(self):
        return self.user_full_name

class VehicleReservation(models.Model):
    YES_NO = (
            ('Y', 'Yes'),
            ('N', 'No'),
    )
    vehicle = models.ForeignKey(Vehicle)
    user = models.ForeignKey(User)
    check_out_dt = models.DateField()
    check_in_dt = models.DateField()
    odometer = models.IntegerField()
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



