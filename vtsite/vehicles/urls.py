from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'vehicles'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^depart$', views.depart, name='depart'),
    url(r'^return$', views.returnFromTrip, name='return'),

]

urlpatterns += staticfiles_urlpatterns()
