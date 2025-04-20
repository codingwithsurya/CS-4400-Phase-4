# flight_manager/api/views.py
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt # Use carefully, consider CSRF protection
from django.views.decorators.http import require_http_methods
from django.db import connection, IntegrityError, DatabaseError
from ..models import Airline, Location # Use relative import

# Import all the operation views
from .views_operations import (
    grant_or_revoke_pilot_license_view,
    offer_flight_view,
    flight_landing_view,
    flight_takeoff_view,
    passengers_board_view,
    passengers_disembark_view,
    assign_pilot_view,
    recycle_crew_view,
    retire_flight_view,
    simulation_cycle_view
)

# Import all the lookup views
from .views_lookups import (
    get_pilots_view,
    get_flights_view,
    get_passengers_view,
    get_routes_view,
    get_pilot_licenses_view,
    get_airplanes_view
)

# --- API Views ---

@csrf_exempt # ONLY for simplicity in testing without frontend CSRF handling. Implement CSRF properly for production.
@require_http_methods(["POST"])
def add_airplane_view(request):
    try:
        data = json.loads(request.body)

        # Extract data matching stored procedure parameters
        # Ensure keys match what the frontend sends (or map them)
        ip_airlineID = data.get('ip_airlineID')
        ip_tail_num = data.get('ip_tail_num')
        ip_seat_capacity = data.get('ip_seat_capacity')
        ip_speed = data.get('ip_speed')
        ip_locationID = data.get('ip_locationID')
        ip_plane_type = data.get('ip_plane_type')
        ip_maintenanced = data.get('ip_maintenanced') # Frontend sends null/true/false
        ip_model = data.get('ip_model')
        ip_neo = data.get('ip_neo') # Frontend sends null/true/false

        # Basic validation (can be more robust)
        if not all([ip_airlineID, ip_tail_num, ip_seat_capacity, ip_speed, ip_locationID, ip_plane_type]):
             return JsonResponse({'detail': 'Missing required fields.'}, status=400)
        if not isinstance(ip_seat_capacity, int) or ip_seat_capacity <= 0:
             return JsonResponse({'detail': 'Invalid seat capacity.'}, status=400)
        if not isinstance(ip_speed, int) or ip_speed <= 0:
             return JsonResponse({'detail': 'Invalid speed.'}, status=400)

        # Call the stored procedure
        with connection.cursor() as cursor:
            # Stored procedures might raise errors if constraints fail
            cursor.callproc('add_airplane', [
                ip_airlineID,
                ip_tail_num,
                ip_seat_capacity,
                ip_speed,
                ip_locationID,
                ip_plane_type,
                ip_maintenanced,
                ip_model,
                ip_neo
            ])
            # Check if the SP modified rows - difficult to check directly without output params
            # Assume success if no exception is raised by the SP/DB

        return JsonResponse({'message': 'Airplane added successfully.'}, status=201) # 201 Created

    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        # Catch potential DB errors (like unique constraint violations from SP)
        # You might get specific MySQL error codes here to provide better feedback
        error_message = str(db_err)
        status_code = 400 # Bad Request likely due to constraint violation
        if "Duplicate entry" in error_message:
             error_message = "Duplicate entry. Tail number might already exist for this airline or location ID is taken."
        elif "foreign key constraint fails" in error_message:
             error_message = "Invalid reference. Ensure Airline ID exists."
             status_code = 404 # Not Found might be suitable too
        else:
             error_message = f"Database error: {error_message}"
             status_code = 500 # Internal Server Error for unexpected DB issues

        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error in add_airplane_view: {e}") # Log the error server-side
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)


@require_http_methods(["GET"])
def get_airlines_view(request):
    try:
        # Fetch distinct airline IDs
        airlines = Airline.objects.values('airlineid').distinct().order_by('airlineid')
        return JsonResponse(list(airlines), safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching airlines: {e}'}, status=500)

@require_http_methods(["GET"])
def get_locations_view(request):
    try:
        # Fetch distinct location IDs
        locations = Location.objects.values('locationid').distinct().order_by('locationid')
        return JsonResponse(list(locations), safe=False)
    except Exception as e:
        return JsonResponse({'detail': f'Error fetching locations: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def add_airport_view(request):
    try:
        data = json.loads(request.body)

        # Extract data matching stored procedure parameters
        ip_airportID = data.get('ip_airportID')
        ip_airport_name = data.get('ip_airport_name')
        ip_city = data.get('ip_city')
        ip_state = data.get('ip_state')
        ip_country = data.get('ip_country')
        ip_locationID = data.get('ip_locationID')

        # Basic validation
        if not all([ip_airportID, ip_airport_name, ip_city, ip_state, ip_country, ip_locationID]):
            return JsonResponse({'detail': 'Missing required fields.'}, status=400)

        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('add_airport', [
                ip_airportID,
                ip_airport_name,
                ip_city,
                ip_state,
                ip_country,
                ip_locationID
            ])

        return JsonResponse({'message': 'Airport added successfully.'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        # Handle database errors
        error_message = str(db_err)
        status_code = 400
        if "Duplicate entry" in error_message:
            error_message = "Duplicate entry. Airport ID or location ID might already exist."
        elif "foreign key constraint fails" in error_message:
            error_message = "Invalid reference. Please check your inputs."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500

        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error in add_airport_view: {e}") # Log the error
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def add_person_view(request):
    try:
        data = json.loads(request.body)

        # Extract data matching stored procedure parameters
        ip_personID = data.get('ip_personID')
        ip_first_name = data.get('ip_first_name')
        ip_last_name = data.get('ip_last_name')
        ip_locationID = data.get('ip_locationID')
        ip_taxID = data.get('ip_taxID')  # Optional - for pilots
        ip_experience = data.get('ip_experience')  # Optional - for pilots
        ip_miles = data.get('ip_miles')  # Optional - for passengers
        ip_funds = data.get('ip_funds')  # Optional - for passengers

        # Basic validation
        if not all([ip_personID, ip_first_name, ip_locationID]):
            return JsonResponse({'detail': 'Missing required fields: personID, first_name, and locationID are required.'}, status=400)

        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('add_person', [
                ip_personID,
                ip_first_name,
                ip_last_name,
                ip_locationID,
                ip_taxID,
                ip_experience,
                ip_miles,
                ip_funds
            ])

        return JsonResponse({'message': 'Person added successfully.'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        # Handle database errors
        error_message = str(db_err)
        status_code = 400
        if "Duplicate entry" in error_message:
            error_message = "Duplicate entry. Person ID or taxID might already exist."
        elif "foreign key constraint fails" in error_message:
            error_message = "Invalid reference. Please check that the location exists."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500

        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error in add_person_view: {e}") # Log the error
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)
