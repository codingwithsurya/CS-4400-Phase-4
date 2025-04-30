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
# AirportApp/urls.py
from django.contrib import admin
from django.urls import path, include # Add include
from flight_manager import views as template_views # Rename to avoid conflicts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', template_views.index, name='index'), # Dashboard
    
    # Database Views
    path('alternative-airport/', template_views.alternative_airport_view, name='alternative_airports'),
    path('flights-in-the-air/', template_views.flights_in_the_air_view, name='flights_in_air'),
    path('flights-on-the-ground/', template_views.flights_on_the_ground_view, name='flights_on_ground'),
    path('people-in-the-air/', template_views.people_in_the_air_view, name='people_in_air'),
    path('people-on-the-ground/', template_views.people_on_the_ground_view, name='people_on_ground'),
    path('route-summary/', template_views.route_summary_view, name='route_summary'),
    
    # Procedure Forms
    path('add-airplane/', template_views.add_airplane_view, name='add_airplane'),
    path('add-airport/', template_views.add_airport_view, name='add_airport'),
    path('add-person/', template_views.add_person_view, name='add_person'),
    path('offer-flight/', template_views.offer_flight_view, name='offer_flight'),
    path('flight-takeoff/', template_views.flight_takeoff_view, name='flight_takeoff'),
    path('flight-landing/', template_views.flight_landing_view, name='flight_landing'),
    path('grant-revoke-license/', template_views.grant_revoke_pilot_license_view, name='grant_revoke_license'),
    path('assign-pilot/', template_views.assign_pilot_view, name='assign_pilot'),
    path('passengers-board/', template_views.passengers_board_view, name='passengers_board'),
    path('passengers-disembark/', template_views.passengers_disembark_view, name='passengers_disembark'),
    path('recycle-crew/', template_views.recycle_crew_view, name='recycle_crew'),
    path('retire-flight/', template_views.retire_flight_view, name='retire_flight'),
    path('simulation-cycle/', template_views.simulation_cycle_view, name='simulation_cycle'),
    path('reset-database/', template_views.reset_database_view, name='reset_database'),
    
    # API urls (for backward compatibility)
    path('api/', include('flight_manager.api.urls')),
]