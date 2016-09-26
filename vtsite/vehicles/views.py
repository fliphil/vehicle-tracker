from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DepartureForm
from .models import Vehicle
from .models import User
from .models import VehicleReservation


def index(request):
    return render(request, 'vehicles/home.html', {})


def test(request, number):
    return render(request, 'vehicles/test.html', {'number': number})


def checkin(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DepartureForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            vehicle_form_data = form.cleaned_data['vehicle']
            user_form_data = form.cleaned_data['user']
            odo_form_data = form.cleaned_data['odometer']

            # Lookup the vehicle and user from database
            vehicle_entry = Vehicle.objects.get(vehicle_desc=vehicle_form_data)
            user_entry = User.objects.get(user_full_name=user_form_data)

            # Create a new reservation
            reservation = VehicleReservation(vehicle=vehicle_entry, user=user_entry,
                                             odometer=odo_form_data)
            reservation.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/home/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DepartureForm()

    return render(request, 'vehicles/checkin.html', {'form': form})


def checkout(request):
    return render(request, 'vehicles/checkout.html', {})
