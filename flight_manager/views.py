from django.shortcuts import render
from django.db import connection

# Create your views here.
from django.urls import path
from . import views
from .models import Airline, Airplane, Airport, Flight, Passenger, Person, Pilot, Route, Location, RoutePath
from django.db.models import Count, Avg, Sum

def index(request):
    return render(request, "base.html")

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