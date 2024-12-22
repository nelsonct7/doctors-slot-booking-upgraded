from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta

from .models import Doctor
from appointment.models import Appointment
from .serializers import DoctorSerializer

def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'doctor') or not request.user.doctor.is_verified:
            raise PermissionDenied("Only verified doctors can access this resource")
        return view_func(request, *args, **kwargs)
    return wrapper

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        doctor = self.get_object()
        date = request.query_params.get('date', datetime.now().date())
        
        # Generate time slots (10 AM to 5 PM, excluding 1-2 PM)
        slots = []
        start_time = datetime.strptime('10:00', '%H:%M').time()
        end_time = datetime.strptime('17:00', '%H:%M').time()
        lunch_start = datetime.strptime('13:00', '%H:%M').time()
        lunch_end = datetime.strptime('14:00', '%H:%M').time()
        
        current_time = start_time
        while current_time < end_time:
            if not (lunch_start <= current_time < lunch_end):
                slot = current_time.strftime('%H:%M')
                # Check if slot is available
                is_booked = Appointment.objects.filter(
                    doctor=doctor,
                    date=date,
                    time_slot=slot
                ).exists()
                if not is_booked:
                    slots.append(slot)
            current_time = (datetime.combine(datetime.min, current_time) + 
                          timedelta(minutes=30)).time()
        
        return Response(slots)

    @action(detail=True, methods=['post'])
    def accept_appointment(self, request, pk=None):
        appointment_id = request.data.get('appointment_id')
        try:
            appointment = Appointment.objects.get(id=appointment_id, doctor=self.get_object())
            appointment.status = 'accepted'
            appointment.save()
            return Response({'status': 'appointment accepted'})
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def reject_appointment(self, request, pk=None):
        appointment_id = request.data.get('appointment_id')
        try:
            appointment = Appointment.objects.get(id=appointment_id, doctor=self.get_object())
            appointment.status = 'rejected'
            appointment.save()
            return Response({'status': 'appointment rejected'})
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, 
                          status=status.HTTP_404_NOT_FOUND)