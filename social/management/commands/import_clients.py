import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from social.models import Client
from social.services import sirene_api


class Command(BaseCommand):
    help = "Importe les clients depuis un CSV et enrichit via l’API INSEE (SIREN)."

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            nargs="?",
            default="clients.csv",
            help="Chemin du fichier CSV (défaut : clients.csv)",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])

        if not csv_path.exists():
            raise CommandError(f"Fichier introuvable : {csv_path}")

        self.stdout.write(self.style.NOTICE(f"Import des clients depuis : {csv_path}"))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        # ---------- OUVERTURE ROBUSTE DU FICHIER ----------
        try:
            f = csv_path.open(newline="", encoding="utf-8-sig")
            reader = csv.DictReader(f, delimiter=";")
            next(reader)  # test encodage
            f.seek(0)
            reader = csv.DictReader(f, delimiter=";")
        except UnicodeDecodeError:
            f = csv_path.open(newline="", encoding="latin-1")
            reader = csv.DictReader(f, delimiter=";")
        # ---------------------------------------------------

        self.stdout.write(self.style.NOTICE(
            f"Colonnes détectées : {reader.fieldnames}"
        ))

        for row in reader:
            # -----------------------
            # Récupération flexible des colonnes
            # -----------------------
            raison_social = (
                (row.get("raison_social") or "").strip()
                or (row.get("RaisonSociale") or "").strip()
                or (row.get("NomDossier") or "").strip()
            )

            siren = (
                (row.get("siren") or row.get("Siren") or "").strip()
            )

            representant_legal = (
                (row.get("representant_legal") or "").strip()
                or (row.get("QualiteRepresentantLegal") or "").strip()
            )

            if not siren or not siren.isdigit() or len(siren) != 9:
                self.stdout.write(self.style.WARNING(
                    f"Ligne ignorée (SIREN invalide) : {row}"
                ))
                skipped_count += 1
                continue

            # ---------- APPEL API INSEE (version PRO : SIREN -> établissement siège) ----------
            data = sirene_api.get_siren_info(siren)
            if not data:
                self.stdout.write(self.style.WARNING(
                    f"Impossible de récupérer les données INSEE pour {siren}"
                ))
                skipped_count += 1
                continue
                            # ---------- EXPLOITATION DU JSON INSEE ----------
            unite_legale = data.get("uniteLegale", {})

            # On récupère le NIC du siège pour reconstruire le SIRET du siège
            nic_siege = unite_legale.get("nicSiegeUniteLegale")
            siret_siege = f"{siren}{nic_siege}" if nic_siege else None

            adresse = {}
            siret_value = siret_siege
            ape_value = unite_legale.get("activitePrincipaleUniteLegale")

            # Si on a pu reconstituer un SIRET, on va chercher l'établissement
            if siret_siege:
                etab_data = sirene_api.get_siret_info(siret_siege)
                if etab_data:
                    etab = etab_data.get("etablissement", {})
                    adresse = etab.get("adresseEtablissement", {})
                    siret_value = etab.get("siret") or siret_siege
                    ape_value = (
                        etab.get("activitePrincipaleEtablissement")
                        or ape_value
                    )

            # Adresse complète (numéro + type voie + libellé voie)
            numero_voie = adresse.get("numeroVoieEtablissement") or ""
            type_voie = adresse.get("typeVoieEtablissement") or ""
            libelle_voie = adresse.get("libelleVoieEtablissement") or ""
            adresse_complete = " ".join(
                part for part in [str(numero_voie), type_voie, libelle_voie] if part
            ) or None

            # ---------- MAPPING VERS TON MODÈLE CLIENT ----------
            client_values = {
                "raison_social": (
                    unite_legale.get("denominationUniteLegale")
                    or raison_social
                ),
                "siren": unite_legale.get("siren", siren),
                "siret": siret_value,
                "ape": ape_value,
                "adress_principale_etablissement": adresse_complete,
                "code_postal": adresse.get("codePostalEtablissement"),
                "ville": adresse.get("libelleCommuneEtablissement"),
                "forme_juridique": unite_legale.get("categorieJuridiqueUniteLegale"),
                "representant_legal": representant_legal,
            }

            client, created = Client.objects.update_or_create(
                siren=siren,
                defaults=client_values,
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Créé : {client.raison_social} ({client.siren})"
                ))
            else:
                updated_count += 1
                self.stdout.write(self.style.NOTICE(
                    f"Mis à jour : {client.raison_social} ({client.siren})"
                ))