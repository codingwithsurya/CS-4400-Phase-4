# flight_manager/api/views.py
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt # Use carefully, consider CSRF protection
from django.views.decorators.http import require_http_methods
from django.db import connection, IntegrityError, DatabaseError
from ..models import Airline, Location # Use relative import

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
