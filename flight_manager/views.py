from django.shortcuts import render, redirect
## Import Mysql
from django.db import connection
from django.contrib import messages

# Create your views here.
from django.urls import path
from . import views
from .models import Airline, Airplane, Airport, Flight, Passenger, Person, Pilot, Route, Location, RoutePath
from django.db.models import Count, Avg, Sum
from .forms import AddAirplaneForm, AddAirportForm, AddPersonForm, OfferFlightForm, FlightActionForm, PilotLicenseForm, AssignPilotForm
from .custom_forms import SafeFlightForm, SafeAssignPilotForm

def index(request):
    return render(request, "index.html")

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

# Form-based views for stored procedures
def add_airplane_view(request):
    if request.method == 'POST':
        form = AddAirplaneForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                cleaned_data = form.cleaned_data
                add_airplane_sp(
                    cleaned_data['ip_airlineID'].airlineid,
                    cleaned_data['ip_tail_num'],
                    cleaned_data['ip_seat_capacity'],
                    cleaned_data['ip_speed'],
                    cleaned_data['ip_locationID'].locationid,
                    cleaned_data['ip_plane_type'],
                    cleaned_data['ip_maintenanced'],
                    cleaned_data['ip_model'],
                    cleaned_data['ip_neo']
                )
                messages.success(request, 'Airplane added successfully!')
                return redirect('flights_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = AddAirplaneForm()
    
    return render(request, 'add_airplane.html', {'form': form})

def add_airport_view(request):
    if request.method == 'POST':
        form = AddAirportForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                cleaned_data = form.cleaned_data
                add_airport_sp(
                    cleaned_data['ip_airportID'],
                    cleaned_data['ip_airport_name'],
                    cleaned_data['ip_city'],
                    cleaned_data['ip_state'],
                    cleaned_data['ip_country'],
                    cleaned_data['ip_locationID'].locationid
                )
                messages.success(request, 'Airport added successfully!')
                return redirect('alternative_airports')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = AddAirportForm()
    
    return render(request, 'add_airport.html', {'form': form})

def add_person_view(request):
    if request.method == 'POST':
        form = AddPersonForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                cleaned_data = form.cleaned_data
                add_person_sp(
                    cleaned_data['ip_personID'],
                    cleaned_data['ip_first_name'],
                    cleaned_data['ip_last_name'],
                    cleaned_data['ip_locationID'].locationid,
                    cleaned_data['ip_taxID'],
                    cleaned_data['ip_experience'],
                    cleaned_data['ip_miles'],
                    cleaned_data['ip_funds']
                )
                messages.success(request, 'Person added successfully!')
                return redirect('people_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = AddPersonForm()
    
    return render(request, 'add_person.html', {'form': form})

def offer_flight_view(request):
    if request.method == 'POST':
        form = OfferFlightForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                cleaned_data = form.cleaned_data
                offer_flight_sp(
                    cleaned_data['ip_flightID'],
                    cleaned_data['ip_routeID'].routeid,
                    cleaned_data['ip_support_airline'].airlineid,
                    cleaned_data['ip_support_tail'].tail_num,
                    cleaned_data['ip_progress'],
                    cleaned_data['ip_next_time'],
                    cleaned_data['ip_cost']
                )
                messages.success(request, 'Flight offered successfully!')
                return redirect('flights_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = OfferFlightForm()
    
    return render(request, 'offer_flight.html', {'form': form})

def flight_takeoff_view(request):
    if request.method == 'POST':
        form = SafeFlightForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                flight_id = form.cleaned_data['ip_flightID']
                flight_takeoff_sp(flight_id)
                messages.success(request, 'Flight takeoff successful!')
                return redirect('flights_in_air')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SafeFlightForm()
    
    return render(request, 'flight_takeoff.html', {'form': form})

def flight_landing_view(request):
    if request.method == 'POST':
        form = SafeFlightForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                flight_id = form.cleaned_data['ip_flightID']
                flight_landing_sp(flight_id)
                messages.success(request, 'Flight landing successful!')
                return redirect('flights_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SafeFlightForm()
    
    return render(request, 'flight_landing.html', {'form': form})

def grant_revoke_pilot_license_view(request):
    if request.method == 'POST':
        form = PilotLicenseForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                person_id = form.cleaned_data['ip_personID'].personid
                license = form.cleaned_data['ip_license']
                grant_or_revoke_pilot_license_sp(person_id, license)
                messages.success(request, 'Pilot license updated successfully!')
                return redirect('people_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = PilotLicenseForm()
    
    return render(request, 'grant_revoke_license.html', {'form': form})

def assign_pilot_view(request):
    if request.method == 'POST':
        form = SafeAssignPilotForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                flight_id = form.cleaned_data['ip_flightID']
                person_id = form.cleaned_data['ip_personID']
                assign_pilot_sp(flight_id, person_id)
                messages.success(request, 'Pilot assigned successfully!')
                return redirect('flights_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SafeAssignPilotForm()
    
    return render(request, 'assign_pilot.html', {'form': form})

def passengers_board_view(request):
    if request.method == 'POST':
        form = SafeFlightForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                flight_id = form.cleaned_data['ip_flightID']
                passengers_board_sp(flight_id)
                messages.success(request, 'Passengers boarded successfully!')
                return redirect('flights_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SafeFlightForm()
    
    return render(request, 'passengers_board.html', {'form': form})

def passengers_disembark_view(request):
    if request.method == 'POST':
        form = SafeFlightForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                flight_id = form.cleaned_data['ip_flightID']
                passengers_disembark_sp(flight_id)
                messages.success(request, 'Passengers disembarked successfully!')
                return redirect('flights_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SafeFlightForm()
    
    return render(request, 'passengers_disembark.html', {'form': form})

def recycle_crew_view(request):
    if request.method == 'POST':
        form = SafeFlightForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                flight_id = form.cleaned_data['ip_flightID']
                recycle_crew_sp(flight_id)
                messages.success(request, 'Crew recycled successfully!')
                return redirect('flights_on_ground')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SafeFlightForm()
    
    return render(request, 'recycle_crew.html', {'form': form})

def retire_flight_view(request):
    if request.method == 'POST':
        form = SafeFlightForm(request.POST)
        if form.is_valid():
            try:
                # Extract data from form
                flight_id = form.cleaned_data['ip_flightID']
                retire_flight_sp(flight_id)
                messages.success(request, 'Flight retired successfully!')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SafeFlightForm()
    
    return render(request, 'retire_flight.html', {'form': form})

def simulation_cycle_view(request):
    if request.method == 'POST':
        try:
            simulation_cycle_sp()
            messages.success(request, 'Simulation cycle completed successfully!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        return redirect('index')
    
    return render(request, 'simulation_cycle.html')