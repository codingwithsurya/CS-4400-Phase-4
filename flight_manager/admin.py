from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Airline, Airplane, Airport, Flight, Passenger, Person, Pilot, Route, Location, RoutePath,PilotLicenses,PassengerVacations

admin.site.register(Airline)
# Says already registered?
#admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Flight)
#admin.site.register(Passenger)
admin.site.register(PassengerVacations)
admin.site.register(Person)
admin.site.register(Pilot)
admin.site.register(PilotLicenses)
admin.site.register(Route)
admin.site.register(Location)
admin.site.register(RoutePath)