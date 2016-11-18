from django.contrib import admin
from .models import Vehicle, TripReservation, UserStatus, VehicleStatus

admin.site.register(Vehicle)
admin.site.register(TripReservation)
admin.site.register(UserStatus)
admin.site.register(VehicleStatus)
