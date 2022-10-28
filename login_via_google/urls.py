import imp
from django import views
from django.urls import include, path
from . import views
urlpatterns = [
    path('login_via_goolge/', views.login_via_goolge, name='login_via_goolge')
]