from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

class SignupView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        user_type = request.data.get('user_type')
        if user_type not in ['doctor', 'patient']:
            return Response({'error': 'Invalid user type'}, 
                          status=status.HTTP_400_BAD_REQUEST)

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
        group = Group.objects.get(name=user_type.capitalize())
        user.groups.add(group)

        # Create profile
        if user_type == 'doctor':
            Doctor.objects.create(user=user)
        else:
            Patient.objects.create(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
