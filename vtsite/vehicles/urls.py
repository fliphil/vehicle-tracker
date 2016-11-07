from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^checkout_vehicle$', views.checkout_vehicle, name='checkout_vehicle'),
    url(r'^checkin_vehicle$', views.checkin_vehicle, name='checkin_vehicle'),
]

urlpatterns += staticfiles_urlpatterns()
