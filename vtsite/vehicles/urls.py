from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from .forms import VehicleForm, TripForm, CheckForm, PostCheckForm
from .views import DepartureFormWizard, ReturnFormWizard


app_name = 'vehicles'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^depart$', DepartureFormWizard.as_view([VehicleForm, TripForm, CheckForm])),
    url(r'^return$', ReturnFormWizard.as_view([PostCheckForm])),
]

urlpatterns += staticfiles_urlpatterns()
