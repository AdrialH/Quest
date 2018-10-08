from django.conf.urls import url
from . import views           


urlpatterns = [
    url(r'^$', views.home),
    url(r'^index$', views.register_page),
    url(r'^login$', views.login_page),
    url(r'^makeaccount$', views.register),
    url(r'^sign_in$', views.login), 
    url(r'^logged$', views.logged),
    url(r'^buyitem$', views.buyitem),
    url(r'^sellitem$', views.sellitem),
    url(r'^view$', views.view),
    url(r'^logout$', views.home),
    url(r'^fight$', views.fight),
    url(r'^create2$', views.create2),
    # url(r'^delete$', views.delete)
]