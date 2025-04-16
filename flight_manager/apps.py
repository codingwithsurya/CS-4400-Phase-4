from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'

class FlightManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flight_manager'
