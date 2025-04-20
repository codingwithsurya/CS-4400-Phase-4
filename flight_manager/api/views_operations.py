# flight_manager/api/views_operations.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection, IntegrityError, DatabaseError

# --- Additional API Views for Flight Operations ---

@csrf_exempt
@require_http_methods(["POST"])
def grant_or_revoke_pilot_license_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_personID = data.get('ip_personID')
        ip_license = data.get('ip_license')
        
        # Basic validation
        if not ip_personID or not ip_license:
            return JsonResponse({'detail': 'Missing required fields.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('grant_or_revoke_pilot_license', [
                ip_personID,
                ip_license
            ])
            
        return JsonResponse({'message': 'Pilot license status updated successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "Duplicate entry" in error_message:
            error_message = "Duplicate entry error."
        elif "foreign key constraint fails" in error_message:
            error_message = "Invalid reference. Please check that all IDs exist."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in grant_or_revoke_pilot_license_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def offer_flight_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        ip_routeID = data.get('ip_routeID')
        ip_support_airline = data.get('ip_support_airline')
        ip_support_tail = data.get('ip_support_tail')
        ip_progress = data.get('ip_progress')
        ip_airplane_status = data.get('ip_airplane_status')
        ip_next_time = data.get('ip_next_time')
        
        # Basic validation
        if not all([ip_flightID, ip_routeID, ip_support_airline, ip_support_tail]):
            return JsonResponse({'detail': 'Missing required fields.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('offer_flight', [
                ip_flightID,
                ip_routeID,
                ip_support_airline,
                ip_support_tail,
                ip_progress,
                ip_airplane_status,
                ip_next_time
            ])
            
        return JsonResponse({'message': 'Flight offered successfully.'}, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "Duplicate entry" in error_message:
            error_message = "Duplicate entry. Flight ID might already exist."
        elif "foreign key constraint fails" in error_message:
            error_message = "Invalid reference. Please check that all IDs exist."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in offer_flight_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def flight_landing_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        
        # Basic validation
        if not ip_flightID:
            return JsonResponse({'detail': 'Flight ID is required.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('flight_landing', [ip_flightID])
            
        return JsonResponse({'message': 'Flight landed successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "not found" in error_message.lower():
            error_message = "Flight not found or cannot be landed."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in flight_landing_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def flight_takeoff_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        
        # Basic validation
        if not ip_flightID:
            return JsonResponse({'detail': 'Flight ID is required.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('flight_takeoff', [ip_flightID])
            
        return JsonResponse({'message': 'Flight took off successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "not found" in error_message.lower():
            error_message = "Flight not found or cannot take off."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in flight_takeoff_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def passengers_board_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        
        # Basic validation
        if not ip_flightID:
            return JsonResponse({'detail': 'Flight ID is required.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('passengers_board', [ip_flightID])
            
        return JsonResponse({'message': 'Passengers boarded successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "not found" in error_message.lower():
            error_message = "Flight not found or not ready for boarding."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in passengers_board_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def passengers_disembark_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        
        # Basic validation
        if not ip_flightID:
            return JsonResponse({'detail': 'Flight ID is required.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('passengers_disembark', [ip_flightID])
            
        return JsonResponse({'message': 'Passengers disembarked successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "not found" in error_message.lower():
            error_message = "Flight not found or not ready for disembarkation."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in passengers_disembark_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def assign_pilot_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        ip_personID = data.get('ip_personID')
        
        # Basic validation
        if not ip_flightID or not ip_personID:
            return JsonResponse({'detail': 'Flight ID and Person ID are required.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('assign_pilot', [ip_flightID, ip_personID])
            
        return JsonResponse({'message': 'Pilot assigned successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "not found" in error_message.lower():
            error_message = "Flight or pilot not found."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in assign_pilot_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def recycle_crew_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        
        # Basic validation
        if not ip_flightID:
            return JsonResponse({'detail': 'Flight ID is required.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('recycle_crew', [ip_flightID])
            
        return JsonResponse({'message': 'Crew recycled successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "not found" in error_message.lower():
            error_message = "Flight not found or not eligible for crew recycling."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in recycle_crew_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def retire_flight_view(request):
    try:
        data = json.loads(request.body)
        
        # Extract parameters
        ip_flightID = data.get('ip_flightID')
        
        # Basic validation
        if not ip_flightID:
            return JsonResponse({'detail': 'Flight ID is required.'}, status=400)
            
        # Call the stored procedure
        with connection.cursor() as cursor:
            cursor.callproc('retire_flight', [ip_flightID])
            
        return JsonResponse({'message': 'Flight retired successfully.'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON.'}, status=400)
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 400
        if "not found" in error_message.lower():
            error_message = "Flight not found or cannot be retired."
            status_code = 404
        else:
            error_message = f"Database error: {error_message}"
            status_code = 500
            
        return JsonResponse({'detail': error_message}, status=status_code)
    except Exception as e:
        print(f"Error in retire_flight_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def simulation_cycle_view(request):
    try:
        # Call the stored procedure without parameters
        with connection.cursor() as cursor:
            cursor.callproc('simulation_cycle', [])
            
        return JsonResponse({'message': 'Simulation cycle completed successfully.'}, status=200)
        
    except (IntegrityError, DatabaseError) as db_err:
        error_message = str(db_err)
        status_code = 500
        return JsonResponse({'detail': f"Database error: {error_message}"}, status=status_code)
    except Exception as e:
        print(f"Error in simulation_cycle_view: {e}")
        return JsonResponse({'detail': f'An unexpected error occurred: {e}'}, status=500)
