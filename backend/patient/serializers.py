from rest_framework import serializers
from ..auth.serializers import UserSerializer
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'