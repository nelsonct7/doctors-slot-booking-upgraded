from rest_framework import serializers
from .models import Doctor
from custom_auth.serializers import UserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'