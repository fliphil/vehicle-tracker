from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<number>[0-9]+)/$', views.test, name='test'),
    url(r'^checkin$', views.checkin, name='checkin'),
    url(r'^checkout$', views.checkout, name='checkout'),
]

urlpatterns += staticfiles_urlpatterns()
