# social/views.py

from django.shortcuts import render, get_object_or_404
from .models import Client
from .services import sirene_api


def dashboard(request, pk=None):
    """
    Page principale du SaaS :
    - à gauche : liste déroulante des dossiers (clients)
    - à droite : détails du dossier sélectionné + salariés
    """
    clients = Client.objects.all().order_by("raison_social")

    current_client = None
    if pk is not None:
        current_client = get_object_or_404(Client, pk=pk)
    elif clients:
        current_client = clients[0]

    context = {
        "clients": clients,
        "client": current_client,
    }
    return render(request, "dashboard.html", context)


def ajouter_entreprise(request):
    """
    Formulaire SIRET + fiche identité INSEE
    """
    entreprise = None
    error = None

    if request.method == "POST":
        siret = request.POST.get("siret", "").strip().replace(" ", "")

        if len(siret) != 14 or not siret.isdigit():
            error = "Le SIRET doit contenir exactement 14 chiffres."
        else:
            # 🔹 ADAPTE CETTE LIGNE AU NOM DE TA FONCTION DANS sirene_api.py
            # Par exemple : get_siret_info, get_siret_data, etc.
            data = sirene_api.get_siret_info(siret)

            if not data:
                error = "Aucune entreprise trouvée pour ce SIRET."
            else:
                etab = data.get("etablissement", data)

                unite_legale = etab.get("uniteLegale", {})
                adresse = etab.get("adresseEtablissement", {})
                periodes = etab.get("periodesEtablissement") or []
                periode = periodes[0] if periodes else {}

                entreprise = {
                    "siren": etab.get("siren"),
                    "siret": etab.get("siret"),
                    "denomination": unite_legale.get("denominationUniteLegale"),
                    "activite_principale": (
                        periode.get("activitePrincipaleEtablissement")
                        or unite_legale.get("activitePrincipaleUniteLegale")
                    ),
                    "naf_nomenclature": (
                        periode.get("nomenclatureActivitePrincipaleEtablissement")
                        or unite_legale.get("nomenclatureActivitePrincipaleUniteLegale")
                    ),
                    "categorie_juridique": unite_legale.get("categorieJuridiqueUniteLegale"),
                    "categorie_entreprise": unite_legale.get("categorieEntreprise"),
                    "date_creation": unite_legale.get("dateCreationUniteLegale"),
                    # Adresse
                    "numero_voie": adresse.get("numeroVoieEtablissement"),
                    "type_voie": adresse.get("typeVoieEtablissement"),
                    "libelle_voie": adresse.get("libelleVoieEtablissement"),
                    "code_postal": adresse.get("codePostalEtablissement"),
                    "commune": adresse.get("libelleCommuneEtablissement"),
                    # Effectifs
                    "tranche_effectifs_etab": etab.get("trancheEffectifsEtablissement"),
                    "annee_effectifs_etab": etab.get("anneeEffectifsEtablissement"),
                    "tranche_effectifs_ul": unite_legale.get("trancheEffectifsUniteLegale"),
                    "annee_effectifs_ul": unite_legale.get("anneeEffectifsUniteLegale"),
                    # Divers
                    "etablissement_siege": etab.get("etablissementSiege"),
                    "etat_admin": unite_legale.get("etatAdministratifUniteLegale"),
                }

    context = {
        "entreprise": entreprise,
        "error": error,
    }
    return render(request, "ajouter_entreprise.html", context)
