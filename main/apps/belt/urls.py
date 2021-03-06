from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home/$', views.home),
    url(r'^home/add_book$', views.add_book),
    url(r'^home/add_book/create$', views.create),
    url(r'^book/(?P<id>\d+)$', views.book),
    url(r'user/(?P<id>\d+)$', views.user),
]