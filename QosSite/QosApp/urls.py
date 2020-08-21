#coding=utf-8

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index),
    url(r'^add-flow/', views.CreateFlow),
    url(r'^add-meter/', views.CreateMeter),
    url(r'^del-flow/', views.DelFlow),
    url(r'^del-meter/', views.DelMeter),
]
