from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        # Check if patient has existing appointment at same time
        existing_appointments = Appointment.objects.filter(
            patient=data['patient'],
            date=data['date'],
            time_slot=data['time_slot'],
            status__in=['pending', 'accepted']
        )
        if existing_appointments.exists():
            raise serializers.ValidationError("You already have an appointment at this time")

        # Check if doctor has existing appointment at same time
        doctor_appointments = Appointment.objects.filter(
            doctor=data['doctor'],
            date=data['date'],
            time_slot=data['time_slot']
        )
        if doctor_appointments.exists():
            raise serializers.ValidationError("This time slot is already booked")

        return data