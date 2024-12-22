from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView({'post': 'create'})),
    path('login/', views.TokenObtainPairView, name='token_obtain_pair'),
]