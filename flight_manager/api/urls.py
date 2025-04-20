# flight_manager/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add-airplane/', views.add_airplane_view, name='api_add_airplane'),
    path('airlines/', views.get_airlines_view, name='api_get_airlines'),
    path('locations/', views.get_locations_view, name='api_get_locations'),
    # Add other API endpoints here...
]