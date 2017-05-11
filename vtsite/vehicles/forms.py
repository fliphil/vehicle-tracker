from django import forms
from .models import Vehicle
from .models import VehicleStatus


class TripBeginForm(forms.Form):
    vehicle = forms.CharField(label='License Plate', max_length=20, required=True)
    destination = forms.CharField(label='Destination', max_length=200, required=True)
    odometer = forms.IntegerField(min_value=0, max_value=500000, required=True)
    is_fuel_full = forms.BooleanField(label='Fuel Tank Filled', required=True)
    were_tires_inspected = forms.BooleanField(label='Tires Inspected', required=True)
    completed_damage_inspection = forms.BooleanField(label='Checked for vehicle damage', required=True)

    def clean(self):
        """
        Check the whole form to make sure it has sane data.
        :return:
        """
        # Get the entered data we want to check
        cleaned_data = super(TripBeginForm, self).clean()
        clean_vehicle = cleaned_data.get("vehicle")
        clean_odometer = cleaned_data.get("odometer")

        # Retrieve the existing vehicle database entry.
        vehicle_entry = Vehicle.objects.get(plate=clean_vehicle)

        # Get the last known value for the odometer.
        prev_odometer = vehicle_entry.odometer

        # The newly entered odometer value cannot be less than it was before.
        if clean_odometer < prev_odometer:
            raise forms.ValidationError(
                'FieldError: Odometer value must be greater than or equal to %(value)s',
                code='invalid',
                params={'value': prev_odometer}
            )


class TripFinishForm(forms.Form):
    vehicle_id = forms.CharField(widget=forms.HiddenInput(), max_length=20, required=True)
    odometer = forms.IntegerField(min_value=0,
                                  max_value=500000,
                                  required=True)
    is_fuel_full = forms.BooleanField(label='Fuel Tank Filled',
                                      required=True)
    trash = forms.BooleanField(label='Is the vehicle free of trash?',
                               required=True)
    damage_or_mechanical_problems = forms.BooleanField(label='Reporting damage or mechanical problems',
                                                       required=True)
    comments = forms.CharField(label='Comments',
                               widget=forms.Textarea(attrs={'rows':4, 'cols': 27}),
                               max_length=500,
                               required=False)

    def clean(self):
        """
        Check the whole form to make sure it has sane data.
        :return:
        """
        # Get the entered data we want to check
        cleaned_data = super(TripFinishForm, self).clean()
        clean_vehicle = cleaned_data.get("vehicle_id")
        clean_post_odometer = cleaned_data.get("odometer")

        # Retrieve the current trip.
        vehicle_entry = Vehicle.objects.get(plate=clean_vehicle)
        vehicle_status_entry = VehicleStatus.objects.get(vehicle=vehicle_entry)
        trip_reservation_entry = vehicle_status_entry.most_recent_trip

        # Get the pre-trip value of the odometer.
        trip_pre_odometer = trip_reservation_entry.pre_odometer

        # The post-trip odometer value cannot be less than the pre-trip value.
        if clean_post_odometer < trip_pre_odometer:
            raise forms.ValidationError(
                'FieldError: Odometer value must be greater than or equal to %(value)s',
                code='invalid',
                params={'value': trip_pre_odometer}
            )
