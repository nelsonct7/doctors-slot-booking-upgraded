from django.contrib import admin

# Register your models here.
from .models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    list_display = [all]

# Register your models here.

admin.site.register(Doctor, DoctorAdmin)