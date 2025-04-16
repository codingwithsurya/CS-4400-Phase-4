from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Airline, Airplane

admin.site.register(Airline)
admin.site.register(Airplane)