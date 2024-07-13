from django.contrib import admin
from .models import EventCategory, Event, EventRegistration
# Register your models here.
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(EventRegistration)