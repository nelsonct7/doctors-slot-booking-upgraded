from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.AppointmentListView.as_view(), name='list-appointment'),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='create-appointment'),
    path('appointments/<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='edit-appointment'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='delete-appointment'),
]