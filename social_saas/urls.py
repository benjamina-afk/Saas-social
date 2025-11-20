from django.contrib import admin
from django.urls import path, include

# on importe directement la vue dashboard de l'app social
from social.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),

    # Page d'accueil = dashboard
    path("", dashboard, name="home"),

    # URLs de l'app "social" (dashboard client, ajout entreprise, etc.)
    path("app/", include("social.urls")),
]