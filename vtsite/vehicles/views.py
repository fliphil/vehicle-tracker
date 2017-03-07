from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Vehicle
from .models import VehicleStatus
from .models import UserStatus
from .models import TripReservation
from .forms import TripBeginForm, TripFinishForm
from django.contrib.auth.decorators import login_required
from enum import Enum


class ViewCodes(Enum):
    OK = 0
    FAIL = 1
    RACE_COND = 2


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
            """
            Error should never happen because a UserStatus
            entry is automatically made for each new user
            by vehicle/signals/handlers.py
            """
            print("error: userstatus does not exist")

        if user_status.on_trip is False:
            vehicles_stats = VehicleStatus.objects.all()
            trip = None
        else:
            vehicles_stats = None
            trip = user_status.most_recent_trip

        return render(request, 'vehicles/home.html', {'user_status': user_status,
                                                      'trip': trip,
                                                      'vehicles_stats': vehicles_stats})

    return HttpResponseRedirect('/')


def process_trip_begin(form, request_user):
    """
    Handle the form received from the departure post request.
    Do some validation and then record the data in a new
    VehicleReservation table entry.
    :param form: Form data.
    :param request_user: Current User attached to this request.
    :return:
    """
    vehicle_form_data = form.cleaned_data['vehicle']
    dest_form_data = form.cleaned_data['destination']
    odo_form_data = form.cleaned_data['odometer']
    fuel_form_data = form.cleaned_data['is_fuel_full']
    tire_form_data = form.cleaned_data['were_tires_inspected']
    damage_form_data = form.cleaned_data['completed_damage_inspection']

    # Lookup the vehicle from database
    vehicle_entry = Vehicle.objects.get(desc=vehicle_form_data)
    # Get the status associated with the vehicle
    vehicle_status = VehicleStatus.objects.get(vehicle=vehicle_entry)

    # Get the status associated with user
    user_status = UserStatus.objects.get(user=request_user)

    # Check for on_trip race condition
    if vehicle_status.on_trip is True:
        return ViewCodes.RACE_COND

    # Create a new reservation
    reservation = TripReservation.objects.create(user=request_user,
                                                 vehicle=vehicle_entry,
                                                 destination=dest_form_data,
                                                 pre_odometer=odo_form_data,
                                                 pre_fuel_check=fuel_form_data,
                                                 pre_tire_check=tire_form_data,
                                                 pre_damage_check=damage_form_data)

    # Update the vehicles status
    vehicle_status.on_trip = True
    vehicle_status.most_recent_trip = reservation
    vehicle_status.save()

    # Update the user status
    user_status.on_trip = True
    user_status.most_recent_trip = reservation
    user_status.save()

    return ViewCodes.OK


def process_trip_finish(form, request_user):
    """
    Handle the form received from the Return post request.
    Do some validation and then record the data in an existing
    VehicleReservation table entry.
    :param form_list: Contains a list of multiple form dicts.
    :param request_user: Current User attached to this request.
    :return:
    """
    odo_form_data = form.cleaned_data['odometer']
    fuel_form_data = form.cleaned_data['is_fuel_full']
    trash_form_data = form.cleaned_data['trash']
    damage_form_data = form.cleaned_data['damage_or_mechanical_problems']
    comments_form_data = form.cleaned_data['comments']

    # Get status associated with the user, contains the current trip data
    user_status = UserStatus.objects.get(user=request_user)

    if user_status.on_trip is True:
        # Get the foreign key id of the TripReservation
        reservation = user_status.most_recent_trip

        # Get the TripReservation entry, update, and finally save
        reservation.post_odometer = odo_form_data
        reservation.post_fuel_check = fuel_form_data
        reservation.post_trash_check = trash_form_data
        reservation.post_damage_check = damage_form_data
        reservation.post_comments = comments_form_data
        reservation.time_check_in = timezone.now()
        reservation.save()

        # Now that the vehicle has been returned, update it's status
        vehicle = reservation.vehicle
        vehicle_status = VehicleStatus.objects.get(vehicle=vehicle)
        vehicle_status.on_trip = False
        vehicle_status.save()

        # Now that the User has returned, update their status
        user_status.on_trip = False
        user_status.save()
    else:
        print("error: user should not have gotten here, not on trip")


@login_required
def trip_begin(request):
    """
    Run this function after a vehicles/trip_begin url redirect.
    :param request: HTTP request from client
    :return: HttpResponse with reservation status page
    """
    if request.method == 'POST':
        if 'flag' in request.POST:
            flag = request.POST['flag']
            if flag == "clicked":
                # Request containing the id of vehicle that was clicked by user
                id_vehicle = request.POST['id_vehicle']
                form = TripBeginForm(initial={'vehicle': id_vehicle})
                return render(request, 'vehicles/trip_begin.html', {'form': form})
            else:
                return HttpResponse(content="error: error: invalid 'flag' value")
        else:
            # create a form instance and populate it with data from the request:
            form = TripBeginForm(request.POST)

            # handle the form data
            if form.is_valid():
                rc = process_trip_begin(form, request.user)

            if rc == ViewCodes.OK:
                # redirect to a new URL:
                return HttpResponseRedirect('/vehicles')
            elif rc == ViewCodes.RACE_COND:
                # Vehicle is no longer available, someone else beat you to the punch!
                # TODO modal message saying the vehicle is no longer available, redirect to vehicle selection
                pass

    # GET (or any other method) is not supported
    else:
        return HttpResponse(content="error: only POST is supported")


@login_required
def trip_finish(request):
    """
    Run this function after a vehicles/trip_finish url redirect.
    :param request: HTTP request from client
    :return: HttpResponse with reservation status page
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TripFinishForm(request.POST)

        # handle the form data
        process_trip_finish(form, request.user)

        # redirect to a new URL:
        return HttpResponseRedirect('/vehicles')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TripFinishForm()

    return render(request, 'vehicles/trip_finish.html', {'form': form})
