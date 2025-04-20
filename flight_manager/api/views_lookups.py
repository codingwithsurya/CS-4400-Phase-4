# flight_manager/api/views_lookups.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection, DatabaseError
from ..models import Airline, Location, Person, Pilot, Flight, Route

# --- Data Lookup API Views ---

@require_http_methods(["GET"])
def get_pilots_view(request):
    try:
        # Query the database for all pilots with necessary details
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.personID, p.first_name, p.last_name, pi.taxID, pi.experience, pi.commanding_flight
                FROM person p
                JOIN pilot pi ON p.personID = pi.personID
                ORDER BY p.personID
            """)
            columns = [col[0] for col in cursor.description]
            pilots = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return JsonResponse(pilots, safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching pilots: {e}'}, status=500)

@require_http_methods(["GET"])
def get_flights_view(request):
    try:
        # Query the database for active flights
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f.flightID, f.routeID, f.support_airline, f.support_tail, f.progress, 
                       f.airplane_status, f.next_time
                FROM flight f
                ORDER BY f.flightID
            """)
            columns = [col[0] for col in cursor.description]
            flights = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return JsonResponse(flights, safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching flights: {e}'}, status=500)

@require_http_methods(["GET"])
def get_passengers_view(request):
    try:
        # Query the database for passengers
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.personID, p.first_name, p.last_name, pa.miles, pa.funds
                FROM person p
                JOIN passenger pa ON p.personID = pa.personID
                ORDER BY p.personID
            """)
            columns = [col[0] for col in cursor.description]
            passengers = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return JsonResponse(passengers, safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching passengers: {e}'}, status=500)

@require_http_methods(["GET"])
def get_routes_view(request):
    try:
        # Query the database for routes
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT r.routeID, r.distance
                FROM route r
                ORDER BY r.routeID
            """)
            columns = [col[0] for col in cursor.description]
            routes = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return JsonResponse(routes, safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching routes: {e}'}, status=500)

@require_http_methods(["GET"])
def get_pilot_licenses_view(request):
    try:
        # Query the database for pilot licenses
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pl.personID, pl.license, p.first_name, p.last_name
                FROM pilot_licenses pl
                JOIN person p ON pl.personID = p.personID
                ORDER BY pl.personID, pl.license
            """)
            columns = [col[0] for col in cursor.description]
            licenses = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return JsonResponse(licenses, safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching pilot licenses: {e}'}, status=500)
