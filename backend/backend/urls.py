"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from appointment import views as appointment_view
from doctor import views as doctor_view
from patient import views as patient_view

router = routers.DefaultRouter()
router.register(r'appointment', appointment_view.AppointmentViewSet, 'appointment')
router.register(r'doctor', doctor_view.DoctorViewSet, 'doctor')
router.register(r'patient', patient_view.PatientViewSet, 'patient')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('custom_auth.urls')),
]
