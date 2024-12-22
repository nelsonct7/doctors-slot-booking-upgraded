from django.contrib import admin

# Register your models here.
from .models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = [all]

# Register your models here.

admin.site.register(Patient, PatientAdmin)