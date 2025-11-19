from django.contrib import admin
from .models import Client, Salarie


class SalarieInline(admin.TabularInline):
    model = Salarie
    extra = 0  # aucune ligne vide en plus
    fields = ("nom", "prenom", "emploi", "qualification", "date_entree")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("raison_social", "forme_juridique", "ville", "code_postal", "email", "telephone")
    search_fields = ("raison_social", "ville", "siret", "siren")
    inlines = [SalarieInline]  # 👈 affiche les salariés dans la fiche du dossier


@admin.register(Salarie)
class SalarieAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "client", "emploi", "qualification", "date_entree")
    search_fields = ("nom", "prenom", "client__raison_social")
    list_filter = ("client", "qualification")
