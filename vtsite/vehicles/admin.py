from django.contrib import admin
from .models import Vehicle, TripReservation, UserStatus, VehicleStatus


class TripReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('time_check_out',)


admin.site.register(Vehicle)
admin.site.register(TripReservation, TripReservationAdmin)
admin.site.register(UserStatus)
admin.site.register(VehicleStatus)
