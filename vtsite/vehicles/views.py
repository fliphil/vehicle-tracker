from django.shortcuts import render
from django.template.context import RequestContext

def index(request):
    return render(request, 'vehicles/home.html', {})

def test(request, number):
    return render(request, 'vehicles/test.html', {'number': number})

def checkin(request):
    return render(request, 'vehicles/checkin.html', {})

def checkout(request):
    return render(request, 'vehicles/checkout.html', {})
