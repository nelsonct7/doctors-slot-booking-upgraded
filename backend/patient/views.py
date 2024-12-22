from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from .models import Patient
from .serializers import PatientSerializer
from ..appointment.serializers import AppointmentSerializer
from ..appointment.models import Appointment

def patient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'patient') or not request.user.patient.is_verified:
            raise PermissionDenied("Only verified patients can access this resource")
        return view_func(request, *args, **kwargs)
    return wrapper

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def book_appointment(self, request, pk=None):
        patient = self.get_object()
        serializer = AppointmentSerializer(data={
            **request.data,
            'patient': patient.id,
            'status': 'pending'
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel_appointment(self, request, pk=None):
        appointment_id = request.data.get('appointment_id')
        try:
            appointment = Appointment.objects.get(id=appointment_id, 
                                               patient=self.get_object())
            appointment.status = 'cancelled'
            appointment.save()
            return Response({'status': 'appointment cancelled'})
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def my_appointments(self, request, pk=None):
        appointments = Appointment.objects.filter(patient=self.get_object())
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)