from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^passengers/$', views.passenger_list, name='passenger_list'),
    url(r'^workspace/$', views.workspace, name='workspace'),
]