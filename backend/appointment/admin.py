from django.contrib import admin

# Register your models here.
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = [all]

# Register your models here.

admin.site.register(Appointment, AppointmentAdmin)