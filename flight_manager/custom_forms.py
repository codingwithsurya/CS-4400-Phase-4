from django import forms
from .models import Flight

class SafeFlightForm(forms.Form):
    """
    A custom form that safely handles potential time format issues in the Flight model.
    """
    ip_flightID = forms.ChoiceField(choices=[], label="Flight")
    
    def __init__(self, *args, **kwargs):
        super(SafeFlightForm, self).__init__(*args, **kwargs)
        # Get flight IDs directly using a raw query to avoid time casting issues
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT flightid FROM flight")
            flight_choices = [(row[0], f"Flight {row[0]}") for row in cursor.fetchall()]
            self.fields['ip_flightID'].choices = flight_choices

class SafeAssignPilotForm(forms.Form):
    """
    A custom form that safely handles assignment of pilots to flights
    """
    ip_flightID = forms.ChoiceField(choices=[], label="Flight")
    ip_personID = forms.ChoiceField(choices=[], label="Pilot")
    
    def __init__(self, *args, **kwargs):
        super(SafeAssignPilotForm, self).__init__(*args, **kwargs)
        # Get data directly using raw queries to avoid ORM issues
        from django.db import connection
        
        # Get flights
        with connection.cursor() as cursor:
            cursor.execute("SELECT flightid FROM flight")
            flight_choices = [(row[0], f"Flight {row[0]}") for row in cursor.fetchall()]
            self.fields['ip_flightID'].choices = flight_choices
            
        # Get pilots
        with connection.cursor() as cursor:
            cursor.execute("SELECT person.personid, concat(first_name, ' ', last_name) as fullname FROM person JOIN pilot ON person.personid = pilot.personid")
            pilot_choices = [(row[0], row[1]) for row in cursor.fetchall()]
            self.fields['ip_personID'].choices = pilot_choices
