# social/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("app/", views.dashboard, name="dashboard"),
    path("app/<int:pk>/", views.dashboard, name="dashboard_client"),
    path("entreprise/ajouter/", views.ajouter_entreprise, name="ajouter_entreprise"),
]
