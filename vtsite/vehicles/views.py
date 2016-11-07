from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DepartureForm
from .models import Vehicle
from .models import User
from .models import TripReservation


def index(request):
    return render(request, 'vehicles/home.html', {})


def receive_checkout_info(form):
    """
    Handle the form received from the checkout_vehicle post
    request. Do some validation and then record the data in a
    new VehicleReservation table entry.
    :param form: Contains the form data.
    :return:
    """
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        vehicle_form_data = form.cleaned_data['vehicle']
        user_form_data = form.cleaned_data['user']
        odo_form_data = form.cleaned_data['odometer']

        # Lookup the vehicle and user from database
        vehicle_entry = Vehicle.objects.get(vehicle_desc=vehicle_form_data)
        user_entry = User.objects.get(user_name=user_form_data)

        # Create a new reservation
        reservation = TripReservation(vehicle=vehicle_entry, user=user_entry,
                                      odometer=odo_form_data)
        reservation.save()


def checkout_vehicle(request):
    """
    Run this function after a vehicles/checkout_vehicles url redirect.
    :param request: HTTP request from client
    :return: HttpResponse with reservation status page
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DepartureForm(request.POST)

        # handle the form data
        receive_checkout_info(form)

        # redirect to a new URL:
        return HttpResponseRedirect('/vehicles')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DepartureForm()

    return render(request, 'vehicles/checkout_vehicle.html', {'form': form})


def checkin_vehicle(request):
    return render(request, 'vehicles/checkin_vehicle.html', {})
