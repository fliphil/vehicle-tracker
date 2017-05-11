from django.conf.urls import url

from . import views

app_name = 'vehicles'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trip_begin$', views.trip_begin, name='trip_begin'),
    url(r'^trip_finish$', views.trip_finish, name='trip_finish'),
    url(r'^race_cond$', views.race_cond, name='race_cond'),
]
