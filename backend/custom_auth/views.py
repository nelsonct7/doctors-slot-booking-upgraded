from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import transaction

from .serializers import UserSerializer
from doctor.models import Doctor
from patient.models import Patient

class SignupView(generics.CreateAPIView):  # Make sure this is CreateAPIView
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'first_name', 
                             'last_name', 'user_type']
            for field in required_fields:
                if not request.data.get(field):
                    return Response(
                        {'error': f'{field} is required'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            user_type = request.data.get('user_type')
            if user_type not in ['doctor', 'patient']:
                return Response(
                    {'error': 'User type must be either doctor or patient'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Create user
            user = User.objects.create(
                username=request.data['username'],
                email=request.data['email'],
                password=make_password(request.data['password']),
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )

            # Add to appropriate group
            try:
                group = Group.objects.get(name=user_type.capitalize())
                user.groups.add(group)
            except Group.DoesNotExist:
                user.delete()
                return Response(
                    {'error': f'Group {user_type} does not exist'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create profile
            if user_type == 'doctor':
                Doctor.objects.create(user=user)
            else:
                Patient.objects.create(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
