from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DepartureForm
from .forms import ArrivalForm
from .models import Vehicle
from .models import UserStatus
from .models import TripReservation


def index(request):
    if request.user.is_authenticated:
        try:
            user_status = UserStatus.objects.get(username=request.user.username)
        except:
            user_status = UserStatus(username=request.user.username)

        if user_status.on_trip == False:
            return HttpResponseRedirect('/vehicles/checkout_vehicle')
        else:
            return HttpResponseRedirect('/vehicles/checkin_vehicle)')

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
        dest_form_data = form.cleaned_data['destination']
        odo_form_data = form.cleaned_data['odometer']
        fuel_form_data = form.cleaned_data['isFuelFull']
        tire_form_data = form.cleaned_data['wereTiresInspected']
        damage_form_data = form.cleaned_data['completedDamageInspection']

        # Lookup the vehicle and user from database
        vehicle_entry = Vehicle.objects.get(vehicle_desc=vehicle_form_data)
        user_entry = User.objects.get(user_name=user_form_data)

        # Create a new reservation
        reservation = TripReservation(vehicle=vehicle_entry, user=user_entry,
                                      odometer=odo_form_data)
        reservation.save()

def receive_checkin_info(form):
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
        dest_form_data = form.cleaned_data['destination']
        odo_form_data = form.cleaned_data['odometer']
        fuel_form_data = form.cleaned_data['isFuelFull']
        trash_form_data = form.cleaned_data['trash']
        damage_form_data = form.cleaned_data['damageOrMechanicalProblems']
        comments_form_data = form.cleaned_data['comments']

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
    if request.user.is_authenticated:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = DepartureForm(request.POST)

            # handle the form data
            receive_checkout_info(form)

            # redirect to a new URL:
            return HttpResponseRedirect('/vehicles')

        # if a GET (or any other method) we'll create a blank form
        else:
            # user_status = UserStatus.objects.get(username=request.user.username)
            form = DepartureForm()

        return render(request, 'vehicles/checkout_vehicle.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def checkin_vehicle(request):
    """
    Run this function after a vehicles/checkin_vehicles url redirect.
    :param request: HTTP request from client
    :return: HttpResponse with reservation status page
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ArrivalForm(request.POST)

            # handle the form data
            receive_checkin_info(form)

            # redirect to a new URL:
            return HttpResponseRedirect('/vehicles')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = ArrivalForm()
        return render(request, 'vehicles/checkin_vehicle.html', {'form': form})
    else:
        return HttpResponseRedirect('/')
