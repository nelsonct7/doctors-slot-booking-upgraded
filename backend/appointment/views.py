# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter appointments based on the user (patient)
        return Appointment.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the patient as the current user
        serializer.save(patient=self.request.user)
