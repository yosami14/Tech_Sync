from django.apps import AppConfig

class EventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event'

    def ready(self):
        # Import the signals module to ensure the signal handlers are registered
        import event.signals
