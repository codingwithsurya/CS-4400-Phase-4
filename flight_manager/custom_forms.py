from django import forms
from .models import Flight

class SafeFlightForm(forms.Form):
    """
    A custom form that provides both dropdown and manual text entry for Flight ID.
    """
    flight_selector = forms.ChoiceField(label="Select Flight", required=False)
    ip_flightID = forms.CharField(label="Or enter Flight ID manually", max_length=50, required=False)
    
    def __init__(self, *args, **kwargs):
        super(SafeFlightForm, self).__init__(*args, **kwargs)
        # Get flight IDs directly using a raw query to avoid time casting issues
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT flightid FROM flight")
            flight_choices = [(row[0], f"Flight {row[0]}") for row in cursor.fetchall()]
            self.fields['flight_selector'].choices = [(None, "---------")] + flight_choices
    
    def clean(self):
        cleaned_data = super().clean()
        flight_selector = cleaned_data.get("flight_selector")
        manual_flightID = cleaned_data.get("ip_flightID")
        
        # Use the selector value if provided, otherwise use the manual entry
        if flight_selector and flight_selector != "None":
            cleaned_data["ip_flightID"] = flight_selector
        elif not manual_flightID:
            raise forms.ValidationError("Please either select a flight or enter a flight ID manually.")
        
        return cleaned_data

class SafeAssignPilotForm(forms.Form):
    """
    A custom form that provides both dropdown and manual text entry for Flight ID and Person ID.
    """
    flight_selector = forms.ChoiceField(label="Select Flight", required=False)
    ip_flightID = forms.CharField(label="Or enter Flight ID manually", max_length=50, required=False)
    
    pilot_selector = forms.ChoiceField(label="Select Pilot", required=False)
    ip_personID = forms.CharField(label="Or enter Pilot ID manually", max_length=50, required=False)
    
    def __init__(self, *args, **kwargs):
        super(SafeAssignPilotForm, self).__init__(*args, **kwargs)
        # Get data directly using raw queries to avoid ORM issues
        from django.db import connection
        
        # Get flights
        with connection.cursor() as cursor:
            cursor.execute("SELECT flightid FROM flight")
            flight_choices = [(row[0], f"Flight {row[0]}") for row in cursor.fetchall()]
            self.fields['flight_selector'].choices = [(None, "---------")] + flight_choices
        
        # Get pilots
        with connection.cursor() as cursor:
            cursor.execute("SELECT person.personid, concat(first_name, ' ', last_name) as fullname FROM person JOIN pilot ON person.personid = pilot.personid")
            pilot_choices = [(row[0], f"{row[0]}") for row in cursor.fetchall()]
            self.fields['pilot_selector'].choices = [(None, "---------")] + pilot_choices
    
    def clean(self):
        cleaned_data = super().clean()
        flight_selector = cleaned_data.get("flight_selector")
        manual_flightID = cleaned_data.get("ip_flightID")
        pilot_selector = cleaned_data.get("pilot_selector")
        manual_personID = cleaned_data.get("ip_personID")
        
        # Handle Flight ID
        if flight_selector and flight_selector != "None":
            cleaned_data["ip_flightID"] = flight_selector
        elif not manual_flightID:
            raise forms.ValidationError("Please either select a flight or enter a flight ID manually.")
        
        # Handle Person ID
        if pilot_selector and pilot_selector != "None":
            cleaned_data["ip_personID"] = pilot_selector
        elif not manual_personID:
            raise forms.ValidationError("Please either select a pilot or enter a pilot ID manually.")
        
        return cleaned_data
