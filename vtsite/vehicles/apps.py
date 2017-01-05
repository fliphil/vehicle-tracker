from django.apps import AppConfig


class VehiclesConfig(AppConfig):
    name = 'vehicles'

    def ready(self):
        # Import the signal handlers
        from .signals import handlers
