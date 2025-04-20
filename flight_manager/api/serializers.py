# flight_manager/api/serializers.py
from rest_framework import serializers
from ..models import Airline, Location, Airplane, Airport, Person, Passenger, Pilot, PilotLicenses, Flight, Route, Leg, RoutePath

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__' # Or list specific fields

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class AirplaneSerializer(serializers.ModelSerializer):
    # To handle the ForeignKey correctly, you might want nested serialization or just show IDs
    airlineid = serializers.CharField(source='airlineid.airlineid') # Show airline ID string
    locationid = serializers.CharField(source='locationid.locationid', allow_null=True) # Show location ID string or null

    class Meta:
        model = Airplane
        fields = ['airlineid', 'tail_num', 'seat_capacity', 'speed', 'locationid', 'plane_type', 'maintenanced', 'model', 'neo']

class AirportSerializer(serializers.ModelSerializer):
    locationid = serializers.CharField(source='locationid.locationid', allow_null=True)
    class Meta:
        model = Airport
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    locationid = serializers.CharField(source='locationid.locationid')
    class Meta:
        model = Person
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    # If you want related Person info:
    # person_details = PersonSerializer(source='personid', read_only=True)
    personid_val = serializers.CharField(source='personid.personid') # Just the ID

    class Meta:
        model = Passenger
        fields = ['personid_val', 'miles', 'funds'] # Adjust as needed

class PilotSerializer(serializers.ModelSerializer):
    # person_details = PersonSerializer(source='personid', read_only=True)
    personid_val = serializers.CharField(source='personid.personid')
    # To show flight ID or null
    commanding_flight_id = serializers.CharField(source='commanding_flight.flightid', allow_null=True)

    class Meta:
        model = Pilot
        # Explicitly list fields to avoid recursion if commanding_flight pointed back
        fields = ['personid_val', 'taxid', 'experience', 'commanding_flight_id']

class PilotLicenseSerializer(serializers.ModelSerializer):
    personid_val = serializers.CharField(source='personid.personid') # Navigate through Person

    class Meta:
        model = PilotLicenses
        fields = ['personid_val', 'license']

class LegSerializer(serializers.ModelSerializer):
     # Use StringRelatedField or SlugRelatedField for simpler representation of FKs
    departure = serializers.SlugRelatedField(slug_field='airportid', read_only=True)
    arrival = serializers.SlugRelatedField(slug_field='airportid', read_only=True)
    class Meta:
        model = Leg
        fields = '__all__'

class RoutePathSerializer(serializers.ModelSerializer):
    leg = LegSerializer(source='legid', read_only=True) # Example of nested serializer

    class Meta:
        model = RoutePath
        fields = ['sequence', 'leg'] # Add legid if you want the ID too

class RouteSerializer(serializers.ModelSerializer):
    # To show related paths (careful with potential large data/performance)
    # paths = RoutePathSerializer(many=True, read_only=True, source='routepath_set') # Check related_name if needed

    class Meta:
        model = Route
        fields = ['routeid'] # Add 'paths' if using nested serializer above

class FlightSerializer(serializers.ModelSerializer):
    # Use SlugRelatedField to just show the ID strings for related objects
    routeid = serializers.CharField(source='routeid.routeid')
    support_airline = serializers.CharField(source='support_airline.airlineid', allow_null=True)
    support_tail = serializers.CharField(source='support_tail.tail_num', allow_null=True)

    # Special handling for the time field that's causing issues
    def to_representation(self, instance):
        """Custom representation to handle time fields safely"""
        ret = super().to_representation(instance)
        # Handle the next_time field safely - avoid time errors
        try:
            if instance.next_time:
                # Ensure hours are valid (0-23) before formatting
                hours = instance.next_time.hour % 24  # Ensure hours are 0-23
                minutes = instance.next_time.minute
                seconds = instance.next_time.second
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                ret['next_time'] = time_str
            else:
                ret['next_time'] = None
        except Exception as e:
            # If there's any error with the time, return None
            print(f"Error processing time: {e}")
            ret['next_time'] = None
        return ret

    class Meta:
        model = Flight
        fields = ['flightid', 'routeid', 'support_airline', 'support_tail', 'progress', 'airplane_status', 'next_time', 'cost']
