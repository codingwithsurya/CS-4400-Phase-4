"""
URL configuration for AirportApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from flight_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('alternative-airport/', views.alternative_airport_view),  
    path('flights-in-the-air/', views.flights_in_the_air_view),
    path('flights-on-the-ground/', views.flights_on_the_ground_view),
    path('people-in-the-air/', views.people_in_the_air_view),
    path('people-on-the-ground/', views.people_on_the_ground_view),  
    path('route-summary/', views.route_summary_view)
    ]