from django import forms
from .models import Airline, Airplane, Airport, Flight, Passenger, Person, Pilot, Route, Location, RoutePath

class AddAirplaneForm(forms.Form):
    ip_airlineID = forms.ModelChoiceField(queryset=Airline.objects.all(), label="Airline")
    ip_tail_num = forms.CharField(max_length=50, label="Tail Number")
    ip_seat_capacity = forms.IntegerField(min_value=1, label="Seat Capacity")
    ip_speed = forms.IntegerField(min_value=1, label="Speed")
    ip_locationID = forms.ModelChoiceField(queryset=Location.objects.all(), label="Location")
    ip_plane_type = forms.CharField(max_length=100, label="Plane Type")
    ip_maintenanced = forms.BooleanField(required=False, label="Maintenance Status")
    ip_model = forms.CharField(max_length=50, required=False, label="Model")
    ip_neo = forms.BooleanField(required=False, label="NEO Status")

class AddAirportForm(forms.Form):
    ip_airportID = forms.CharField(max_length=3, label="Airport ID")
    ip_airport_name = forms.CharField(max_length=100, label="Airport Name")
    ip_city = forms.CharField(max_length=50, label="City")
    ip_state = forms.CharField(max_length=50, required=False, label="State")
    ip_country = forms.CharField(max_length=50, label="Country")
    ip_locationID = forms.ModelChoiceField(queryset=Location.objects.all(), label="Location")

class AddPersonForm(forms.Form):
    ip_personID = forms.CharField(max_length=50, label="Person ID")
    ip_first_name = forms.CharField(max_length=100, label="First Name")
    ip_last_name = forms.CharField(max_length=100, label="Last Name")
    ip_locationID = forms.ModelChoiceField(queryset=Location.objects.all(), label="Location")
    ip_taxID = forms.CharField(max_length=50, required=False, label="Tax ID")
    ip_experience = forms.IntegerField(required=False, min_value=0, label="Experience")
    ip_miles = forms.IntegerField(required=False, min_value=0, label="Miles")
    ip_funds = forms.DecimalField(required=False, min_value=0, decimal_places=2, label="Funds")

class OfferFlightForm(forms.Form):
    ip_flightID = forms.CharField(max_length=50, label="Flight ID")
    ip_routeID = forms.ModelChoiceField(queryset=Route.objects.all(), label="Route")
    ip_support_airline = forms.ModelChoiceField(queryset=Airline.objects.all(), label="Support Airline")
    ip_support_tail = forms.ModelChoiceField(queryset=Airplane.objects.all(), label="Support Tail")
    ip_progress = forms.IntegerField(min_value=0, label="Progress")
    ip_next_time = forms.IntegerField(min_value=0, label="Next Time")
    ip_cost = forms.DecimalField(min_value=0, decimal_places=2, label="Cost")

class FlightActionForm(forms.Form):
    ip_flightID = forms.ModelChoiceField(queryset=Flight.objects.all(), label="Flight")

class PilotLicenseForm(forms.Form):
    ip_personID = forms.ModelChoiceField(queryset=Person.objects.all(), label="Person")
    ip_license = forms.CharField(max_length=100, label="License")

class AssignPilotForm(forms.Form):
    ip_flightID = forms.ModelChoiceField(queryset=Flight.objects.all(), label="Flight")
    ip_personID = forms.ModelChoiceField(queryset=Person.objects.filter(pilot__isnull=False), label="Pilot")
