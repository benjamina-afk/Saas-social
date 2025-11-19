# social/management/commands/import_clients.py

import csv
from django.core.management.base import BaseCommand
from social.models import Client  # ✅ ton app s'appelle "social"


class Command(BaseCommand):
    help = "Import des clients depuis un fichier CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            nargs="?",
            default="C:\\Users\\benjamin abergel\\saas-social\\clients.csv",
            help="Chemin du fichier CSV des clients",
        )

    def handle(self, *args, **options):
        print(">>> IMPORT CLIENTS LANCÉ DEPUIS social.management.commands.import_clients")

        csv_path = options["csv_path"]
        self.stdout.write(f"Import des clients depuis : {csv_path}")

        created = 0
        updated = 0

        try:
            with open(csv_path, newline="", encoding="latin-1") as f:
                reader = csv.DictReader(f, delimiter=";")

                self.stdout.write(f"Colonnes détectées : {reader.fieldnames}")

                for row in reader:
                    raison_sociale = row.get("RaisonSociale")
                    if not raison_sociale:
                        self.stdout.write("Ligne ignorée : pas de RaisonSociale")
                        continue

                    raw_siret = (row.get("Siret") or "").strip()
                    siret = raw_siret.replace(" ", "")

                    client, created_obj = Client.objects.update_or_create(
                        siret=siret,
                        defaults={
                            "raison_social": raison_sociale,
                            "nom": raison_sociale,
                            "adress_principale_etablissement": row.get("adressPrincipalEtablisst") or "",
                            "capital_euros": row.get("capitalEuros") or 0,
                            "email": row.get("Email") or "",
                            "forme_juridique": row.get("formeJuridique") or "",
                            "nb_titres": row.get("nbTitres") or 0,
                            "nom_dossier": row.get("nomDossier") or "",
                            "qualite_representant1": row.get("QualiteRepresentantLegal") or "",
                            "representant_legal": row.get("RepresentantLegal") or "",
                            "type_titres": row.get("typeTitres") or "",
                            "val_nom_titre": row.get("ValNomTitresEuro") or 0,
                            "activite": row.get("Activite") or "",
                            "adresse1": row.get("Adresse1") or "",
                            "ape": row.get("Ape") or "",
                            "code_postal": row.get("CodePostal") or "",
                            "siren": row.get("Siren") or "",
                            "telephone": row.get("Telephone") or "",
                            "ville": row.get("Ville") or "",
                        },
                    )

                    if created_obj:
                        created += 1
                    else:
                        updated += 1

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fichier introuvable : {csv_path}"))
            return

        self.stdout.write(f"Import terminé. {created} créés, {updated} mis à jour.")
