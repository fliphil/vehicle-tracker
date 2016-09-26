from django.db import models

# Create your models here.
class Vehicle(models.Model):
    vechile_desc models.CharField(max_length=250)

class User(models.Model):
    user_full_name = models.CharField(max_length=50)
    user_password_hash = models.CharField(max_length=64)

class VehicleReservation(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    user = models.ForeignKey(User)
    check_out_dt = models.DateField()
    check_in_dt = models.DateField()
    odometer = models.IntegerField()
    destination = models.CharField(max_length=250)


