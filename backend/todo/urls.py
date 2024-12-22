from django.urls import path

from . import views

urlpatterns = [
    path("/<user>", views.index, name="list-appointment"),
    path("create", views.create_appointment, name="create-appointment"),
    path("edit/<pk>", views.edit_appointment, name="edit-appointment"),
    path("delete/<pk>", views.delete_appointment, name="delete-appointment"),
]