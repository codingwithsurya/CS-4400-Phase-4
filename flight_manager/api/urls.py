# flight_manager/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Create endpoints
    path('add-airplane/', views.add_airplane_view, name='api_add_airplane'),
    path('add-airport/', views.add_airport_view, name='api_add_airport'),
    path('add-person/', views.add_person_view, name='api_add_person'),
    
    path('grant-revoke-pilot-license/', views.grant_or_revoke_pilot_license_view, name='api_grant_revoke_pilot_license'),
    path('offer-flight/', views.offer_flight_view, name='api_offer_flight'),
    path('flight-landing/', views.flight_landing_view, name='api_flight_landing'),
    path('flight-takeoff/', views.flight_takeoff_view, name='api_flight_takeoff'),
    path('passengers-board/', views.passengers_board_view, name='api_passengers_board'),
    path('passengers-disembark/', views.passengers_disembark_view, name='api_passengers_disembark'),
    path('assign-pilot/', views.assign_pilot_view, name='api_assign_pilot'),
    path('recycle-crew/', views.recycle_crew_view, name='api_recycle_crew'),
    path('retire-flight/', views.retire_flight_view, name='api_retire_flight'),
    path('simulation-cycle/', views.simulation_cycle_view, name='api_simulation_cycle'),
    
    # Data lookup endpoints
    path('airlines/', views.get_airlines_view, name='api_get_airlines'),
    path('locations/', views.get_locations_view, name='api_get_locations'),
    path('pilots/', views.get_pilots_view, name='api_get_pilots'),
    path('flights/', views.get_flights_view, name='api_get_flights'),
    path('passengers/', views.get_passengers_view, name='api_get_passengers'),
    path('routes/', views.get_routes_view, name='api_get_routes'),
    path('pilot-licenses/', views.get_pilot_licenses_view, name='api_get_pilot_licenses'),
]