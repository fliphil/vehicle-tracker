import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Vehicle
from .models import VehicleStatus
from .models import UserStatus
from .models import TripReservation
from formtools.wizard.views import SessionWizardView


def index(request):
    """
    The home page for any user that is signed in.
    :param request: Http GET request
    :return:
    """
    if request.user.is_authenticated:
        try:
            user_status = UserStatus.objects.get(user=request.user)
        except ObjectDoesNotExist:
            # error should never happen
            print("error: userstatus does not exist")

        if user_status.on_trip is False:
            return HttpResponseRedirect('/vehicles/depart')
        else:
            return HttpResponseRedirect('/vehicles/return')

    return HttpResponseRedirect('/')



def process_departure_form(form_dict, request_user):
    """
    Handle the form received from the departure post request.
    Do some validation and then record the data in a new
    VehicleReservation table entry.
    :param form_dict: Contains a list of multiple form dicts.
    :param request_user: Current User attached to this request.
    :return:
    """
    vehicle_form_data = form_dict['0'].cleaned_data['vehicle'] # because the Vehicle form is the first in the list of forms... will clean this up later
    dest_form_data = form_dict['1'].cleaned_data['destination']
    odo_form_data = form_dict['2'].cleaned_data['odometer']
    fuel_form_data = form_dict['2'].cleaned_data['is_fuel_full']
    tire_form_data = form_dict['2'].cleaned_data['were_tires_inspected']
    damage_form_data = form_dict['2'].cleaned_data['completed_damage_inspection']

    # Lookup the vehicle from database
    vehicle_entry = Vehicle.objects.get(vehicle_desc=vehicle_form_data)
    # Get the status associated with the vehicle
    vehicle_status = VehicleStatus.objects.get(vehicle=vehicle_entry)

    # Get the status associated with user
    user_status = UserStatus.objects.get(user=request_user)

    # Create a new reservation
    reservation = TripReservation(user=request_user,
                                  vehicle=vehicle_entry,
                                  odometer=odo_form_data)
    reservation.save()

    # Update the vehicles status
    vehicle_status.on_trip = True
    vehicle_status.most_recent_trip = reservation
    vehicle_status.save()

    # Update the user status
    user_status.on_trip = True
    user_status.most_recent_trip = reservation
    user_status.save()


def process_return_form(form_dict, request_user):
    """
    Handle the form received from the Return post request.
    Do some validation and then record the data in an existing
    VehicleReservation table entry.
    :param form_list: Contains a list of multiple form dicts.
    :param request_user: Current User attached to this request.
    :return:
    """
    odo_form_data = form_dict['0'].cleaned_data['odometer']
    fuel_form_data = form_dict['0'].cleaned_data['is_fuel_full']
    trash_form_data = form_dict['0'].cleaned_data['trash']
    damage_form_data = form_dict['0'].cleaned_data['damage_or_mechanical_problems']
    comments_form_data = form_dict['0'].cleaned_data['comments']

    # Get status associated with the user, contains the current trip data
    user_status = UserStatus.objects.get(user=request_user)

    if user_status.on_trip is True:
        # Get the foreign key id of the TripReservation
        user_fk = user_status.most_recent_trip

        # Get the TripReservation entry, update, and finally save
        reservation = TripReservation.objects.get(id=user_fk)
        reservation.time_check_in = datetime.datetime()
        reservation.save()

        # Now that the vehicle has been returned, update it's status
        vehicle_fk = reservation.vehicle
        vehicle = Vehicle.objects.get(id=vehicle_fk)
        vehicle_status = VehicleStatus.objects.get(vehicle=vehicle)
        vehicle_status.on_trip = False
        vehicle_status.save()

        # Now that the User has returned, update their status
        user_status.on_trip = False
        user_status.save()
    else:
        print("error: user should not have gotten here, not on trip")


class DepartureFormWizard(SessionWizardView):
    template_name = "vehicles/home.html"

    def done(self, form_list, form_dict, **kwargs):
        """
        This method will be invoked after the completion of a multi-step Departure Form.
        :param form_list: list of forms holding data gathered during the multi-step process
        :param kwargs:
        :return:
        """
        process_departure_form(form_dict, request_user=self.request.user)
        return HttpResponseRedirect('/')


class ReturnFormWizard(SessionWizardView):
    template_name = "vehicles/home.html"

    def done(self, form_list, form_dict, **kwargs):
        """
        This method will be invoked after the completion of a multi-step Return Form.
        :param form_list: list of forms holding data gathered during the multi-step process
        :param kwargs:
        :return:
        """
        process_return_form(form_dict, request_user=self.request.user)
        return HttpResponseRedirect('/')
