# flight_manager/api/views_lookups.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection, DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Airline, Location, Person, Pilot, Flight, Route, Airplane, Passenger, PilotLicenses
from .serializers import (AirlineSerializer, LocationSerializer, PersonSerializer, 
                          PilotSerializer, FlightSerializer, RouteSerializer, 
                          AirplaneSerializer, PassengerSerializer, PilotLicenseSerializer)

# --- Data Lookup API Views ---

@api_view(['GET'])
def get_pilots_view(request):
    """
    API view to retrieve a list of pilots with their details.
    """
    try:
        # Use Django ORM with select_related to fetch related Person data efficiently
        pilots = Pilot.objects.select_related('personid').all()
        serializer = PilotSerializer(pilots, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_pilots_view: {e}")
        return Response({'detail': f'Error fetching pilots: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_flights_view(request):
    try:
        # Use a raw SQL query to avoid ORM time parsing issues
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f.flightID, f.routeID, f.support_airline, f.support_tail, 
                       f.progress, f.airplane_status, 
                       TIME_FORMAT(f.next_time, '%H:%i:%s') as next_time, 
                       f.cost
                FROM flight f
            """)
            columns = [col[0] for col in cursor.description]
            flights = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return JsonResponse(flights, safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching flights: {str(e)}'}, status=500)

@api_view(['GET'])
def get_passengers_view(request):
    """
    API view to retrieve a list of passengers with their details.
    """
    try:
        # Use Django ORM with select_related for efficient queries
        passengers = Passenger.objects.select_related('personid').all()
        serializer = PassengerSerializer(passengers, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_passengers_view: {e}")
        return Response({'detail': f'Error fetching passengers: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_routes_view(request):
    """
    API view to retrieve a list of routes.
    """
    try:
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_routes_view: {e}")
        return Response({'detail': f'Error fetching routes: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_pilot_licenses_view(request):
    """
    API view to retrieve pilot licenses.
    """
    try:
        licenses = PilotLicenses.objects.select_related('personid', 'personid__personid').all()
        serializer = PilotLicenseSerializer(licenses, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_pilot_licenses_view: {e}")
        return Response({'detail': f'Error fetching pilot licenses: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_airplanes_view(request):
    """
    API view to retrieve a list of airplanes.
    """
    try:
        airplanes = Airplane.objects.all()
        serializer = AirplaneSerializer(airplanes, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_airplanes_view: {e}")
        return Response({'detail': f'Error fetching airplanes: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
