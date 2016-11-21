from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Vehicle
from .models import UserStatus
from .models import TripReservation
from formtools.wizard.views import SessionWizardView

def index(request):
    if request.user.is_authenticated:
        try:
            user_status = UserStatus.objects.get(username=request.user.username)
        except:
            user_status = UserStatus(username=request.user.username)

        if user_status.on_trip == False:
            return HttpResponseRedirect('/vehicles/depart')
        else:
            return HttpResponseRedirect('/vehicles/return')

    return render(request, 'vehicles/home.html', {})


def process_departure_form(form_dict):
    """
    Handle the form received from the departure post
    request. Do some validation and then record the data in a
    new VehicleReservation table entry.
    :param form_dict: Contains the form data.
    :return:
    """
    vehicle_form_data = form_dict[0].cleaned_data['vehicle'] # because the Vehicle form is the first in the list of forms... will clean this up later
    dest_form_data = form_dict[1].cleaned_data['destination']
    odo_form_data = form_dict[2].cleaned_data['odometer']
    fuel_form_data = form_dict[2].cleaned_data['is_fuel_full']
    tire_form_data = form_dict[2].cleaned_data['were_tires_inspected']
    damage_form_data = form_dict[2].cleaned_data['completed_damage_inspection']

    # Lookup the vehicle and user from database
    vehicle_entry = Vehicle.objects.get(vehicle_desc=vehicle_form_data)

    # Create a new reservation
    reservation = TripReservation(vehicle=vehicle_entry,
                                  odometer=odo_form_data)
    reservation.save()

def process_return_form(form_list):
    return


class DepartureFormWizard(SessionWizardView):
    template_name = "vehicles/home.html"

    def done(self, form_list, **kwargs):
        process_departure_form(form_list)
        return HttpResponseRedirect('/')


class ReturnFormWizard(SessionWizardView):
    template_name = "vehicles/home.html"

    def done(self, form_list, form_dict, **kwargs):
        process_return_form(form_dict)
        return HttpResponseRedirect('/')
