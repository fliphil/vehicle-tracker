from django.shortcuts import render


def index(request):
    return render(request, "vehicles/index.html", {})

def test(request, number):
    return render(request, 'vehicles/test.html', {'number': number})
