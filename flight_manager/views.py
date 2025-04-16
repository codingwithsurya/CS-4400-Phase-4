from django.shortcuts import render
from django.db import connection


# Create your views here.
from django.urls import path
from . import views
from .models import Airline, Airplane, Airport, Flight, Passenger, Person, Pilot, Route, Location, RoutePath
from django.db.models import Count, Avg, Sum

def index(request):
    return render(request, "base.html")

## Display all flights
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flight_list.html', {'flights': flights})

## Display airport info
def airport_detail(request, airport_id):
    airport = Airport.objects.get(airportid=airport_id)
    return render(request, 'airport_detail.html', {'airport': airport})

## ******* Stored Procedures *******
## After testing, convert to single function with sp as input

## Offer_flight
def offer_flight_sp(input_flight_number):
    with connection.cursor() as db_call:
        db_call.execute("call flight_landing(%s)", [input_flight_number])
        data_result = db_call.fetchall()
    return data_result

## Flight_landing
def flight_landing_sp(input_flight_number):
    with connection.cursor() as db_call:
        db_call.execute("call flight_landing(%s)", [input_flight_number])
        sp_result = db_call.fetchall()
    return sp_result

## Flight_takeoff
def flight_takeoff_sp(input_flight_number):
    with connection.cursor() as db_call:
        db_call.execute("call flight_takeoff(%s)", [input_flight_number])
        sp_result = db_call.fetchall()
    return sp_result

## Grant or Revoke pilot license
def flight_takeoff_sp(person_id, license):
    with connection.cursor() as db_call:
        db_call.execute("call grant_or_revoke_pilot_license(%s)", [person_id, license])
        sp_result = db_call.fetchall()
    return sp_result

## ******* Views *******
## After testing, convert to single function with view as input

def alternative_airport_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from alternative_airports;")
        row_values = db_call.fetchall()
        column_values = [col[0] for col in db_call.description]
    return render(request, 'alternative_airport.html', {'columns': column_values,'data': row_values})

def flights_in_the_air_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from flights_in_the_air;")
        row_values = db_call.fetchall()
        column_values = [col[0] for col in db_call.description]
    return render(request, 'flights_in_the_air.html', {'columns': column_values,'data': row_values})

def flights_on_the_ground_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from flights_on_the_ground;")
        row_values = db_call.fetchall()
        column_values = [col[0] for col in db_call.description]
    return render(request, 'flights_on_the_ground.html', {'columns': column_values,'data': row_values})

def people_in_the_air_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from people_in_the_air;")
        row_values = db_call.fetchall()
        column_values = [col[0] for col in db_call.description]
    return render(request, 'people_in_the_air.html', {'columns': column_values,'data': row_values})

def people_on_the_ground_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from people_on_the_ground;")
        row_values = db_call.fetchall()
        column_values = [col[0] for col in db_call.description]
    return render(request, 'people_on_the_ground.html', {'columns': column_values,'data': row_values})

def route_summary_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from route_summary;")
        rows = db_call.fetchall()
        columns = [col[0] for col in db_call.description]
    return render(request, 'route_summary.html', {'columns': columns,'data': rows})

## ******* Test Functions *******

## Airlines
airlines = Airline.objects.all()

## Filter for Airbus, boeing
airline = Airline.objects.get(airlineid='Air_France')

# Filter airports by country
us_airports = Airport.objects.filter(country='USA')

# Get flights with specific conditions
active_flights = Flight.objects.filter(airplane_status='in_flight')

# Get passengers with more than 10000 miles
frequent_passengers = Passenger.objects.filter(miles__gt=100)

# Count how many airplanes each airline has
airlines_with_counts = Airline.objects.annotate(num_airplanes=Count('airplane'))

# Get the average miles for all passengers
avg_miles = Passenger.objects.aggregate(avg_miles=Avg('miles'))

# Get all pilots for a specific flight
flight = Flight.objects.get(flightid='aa_12')
pilots = Pilot.objects.filter(commanding_flight=flight)

# Get all airplanes at a specific location
location = Location.objects.get(locationid='plane_1')
airplanes = Airplane.objects.filter(locationid=location)

# Get all legs in a route
route = Route.objects.get(routeid='americas_one')
route_paths = RoutePath.objects.filter(routeid=route).order_by('sequence')
legs = [rp.legid for rp in route_paths]