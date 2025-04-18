from django.shortcuts import render
## Import Mysql
from django.db import connection

# Create your views here.
from django.urls import path
from . import views
from .models import Airline, Airplane, Airport, Flight, Passenger, Person, Pilot, Route, Location, RoutePath
from django.db.models import Count, Avg, Sum

def index(request):
    return render(request, "base.html")

## ******* Stored Procedures *******
## After testing, convert to improved function with sp as input

## Add_airplane
def add_airplane_sp(ip_airlineID, ip_tail_num, ip_seat_capacity, ip_speed, ip_locationID, ip_plane_type, ip_maintenanced, ip_model, ip_neo):
    with connection.cursor() as db_call:
        db_call.execute("call add_airplane(%s, %s, %s, %s, %s, %s, %s)", [ip_airlineID, ip_tail_num, ip_seat_capacity, ip_speed, ip_locationID, ip_plane_type, ip_maintenanced, ip_model, ip_neo])

## Add_airport
def add_airport_sp(ip_airportID, ip_airport_name, ip_city, ip_state, ip_country, ip_locationID):
    with connection.cursor() as db_call:
        db_call.execute("call add_airport(%s, %s, %s, %s, %s, %s)", [ip_airportID, ip_airport_name, ip_city, ip_state, ip_country, ip_locationID])

## Add_person
def add_person_sp(ip_personID, ip_first_name, ip_last_name, ip_locationID, ip_taxID, ip_experience, ip_miles, ip_funds):
    with connection.cursor() as db_call:
        db_call.execute("call add_airplane(%s, %s, %s, %s, %s, %s, %s, %s)", [ip_personID, ip_first_name, ip_last_name, ip_locationID, ip_taxID, ip_experience, ip_miles, ip_funds])

## Offer_flight
def offer_flight_sp(ip_flightID, ip_routeID, ip_support_airline, ip_support_tail, ip_progress, ip_next_time, ip_cost):
    with connection.cursor() as db_call:
        db_call.execute("call flight_landing(%s, %s, %s, %s, %s, %s, %s)", [ip_flightID, ip_routeID, ip_support_airline, ip_support_tail, ip_progress, ip_next_time, ip_cost ])

## Flight_landing
def flight_landing_sp(ip_flightID):
    with connection.cursor() as db_call:
        db_call.execute("call flight_landing(%s)", [ip_flightID])

## Flight_takeoff
def flight_takeoff_sp(ip_flightID):
    with connection.cursor() as db_call:
        db_call.execute("call flight_takeoff(%s)", [ip_flightID])

## Grant or Revoke pilot license
def grant_or_revoke_pilot_license_sp(ip_personID, ip_license):
    with connection.cursor() as db_call:
        db_call.execute("call grant_or_revoke_pilot_license(%s)", [ip_personID, ip_license])

## Assign Pilot
def assign_pilot_sp(ip_flightID, ip_personID):
    with connection.cursor() as db_call:
        db_call.execute("call assign_pilot(%s)", [ip_flightID, ip_personID])

## Passengers_Board
def passengers_board_sp(ip_flightID):
    with connection.cursor() as db_call:
        db_call.execute("call passengers_board(%s)", [ip_flightID])

## Passengers_disembark
def passengers_disembark_sp(ip_flightID):
    with connection.cursor() as db_call:
        db_call.execute("call passengers_disembark(%s)", [ip_flightID])

## Recycle_crew
def recycle_crew_sp(ip_flightID):
    with connection.cursor() as db_call:
        db_call.execute("call recycle_crew(%s)", [ip_flightID])

## Retire_flight
def retire_flight_sp(ip_flightID):
    with connection.cursor() as db_call:
        db_call.execute("call retire_flight(%s);", [ip_flightID])

## simulation_cycle
def simulation_cycle_sp():
    with connection.cursor() as db_call:
        db_call.execute("call simulation_cycle();")


## ******* Views *******
## After testing, can convert to single function with view name as input 

## Alternative Airport view
def alternative_airport_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from alternative_airports;")
        row_values = db_call.fetchall()
        colNames=[]
        for i in db_call.description:
            colNames.append(i[0])
    return render(request, 'alternative_airport.html', {'columns': colNames,'data': row_values})

## Flights in air view
def flights_in_the_air_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from flights_in_the_air;")
        row_values = db_call.fetchall()
        colNames=[]
        for i in db_call.description:
            colNames.append(i[0])    
    return render(request, 'flights_in_the_air.html', {'columns': colNames,'data': row_values})

## flights on ground view
def flights_on_the_ground_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from flights_on_the_ground;")
        row_values = db_call.fetchall()
        colNames=[]
        for i in db_call.description:
            colNames.append(i[0])      
    return render(request, 'flights_on_the_ground.html', {'columns': colNames,'data': row_values})

## People in air view
def people_in_the_air_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from people_in_the_air;")
        row_values = db_call.fetchall()
        colNames=[]
        for i in db_call.description:
            colNames.append(i[0])       
        return render(request, 'people_in_the_air.html', {'columns': colNames,'data': row_values})

## People on ground view
def people_on_the_ground_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from people_on_the_ground;")
        row_values = db_call.fetchall()
        colNames=[]
        for i in db_call.description:
            colNames.append(i[0])     
    return render(request, 'people_on_the_ground.html', {'columns': colNames,'data': row_values})

## route summary view
def route_summary_view(request):
    with connection.cursor() as db_call:
        db_call.execute("select * from route_summary;")
        row_values = db_call.fetchall()
        colNames=[]
        for i in db_call.description:
            colNames.append(i[0])      
    return render(request, 'route_summary.html', {'columns': colNames,'data': row_values})