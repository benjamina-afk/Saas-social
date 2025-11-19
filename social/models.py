from django.db import models


class Client(models.Model):
    raison_social = models.CharField(max_length=255, blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    adress_principale_etablissement = models.CharField(max_length=255, blank=True, null=True)
    capital_euros = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    forme_juridique = models.CharField(max_length=255, blank=True, null=True)
    nb_titres = models.IntegerField(blank=True, null=True)
    nom_dossier = models.CharField(max_length=255, blank=True, null=True)
    qualite_representant1 = models.CharField(max_length=255, blank=True, null=True)
    representant_legal = models.CharField(max_length=255, blank=True, null=True)
    type_titres = models.CharField(max_length=255, blank=True, null=True)
    val_nom_titre = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    activite = models.CharField(max_length=255, blank=True, null=True)
    adresse1 = models.CharField(max_length=255, blank=True, null=True)
    ape = models.CharField(max_length=50, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    siren = models.CharField(max_length=20, blank=True, null=True)
    siret = models.CharField(max_length=20, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"


# social/models.py

class Salarie(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="salaries")

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    nom_marital = models.CharField(max_length=100, blank=True, null=True)
    code_civilite = models.CharField(max_length=10, blank=True, null=True)

    date_naissance = models.DateField(blank=True, null=True)
    commune_naissance = models.CharField(max_length=100, blank=True, null=True)
    code_commune_naissance = models.CharField(max_length=10, blank=True, null=True)
    pays_naissance = models.CharField(max_length=100, blank=True, null=True)

    numero_securite_sociale = models.CharField(max_length=20)
    nationalite = models.CharField(max_length=50, blank=True, null=True)

    num_voie = models.CharField(max_length=10, blank=True, null=True)
    nom_voie = models.CharField(max_length=255, blank=True, null=True)
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)

    code_reglement = models.CharField(max_length=30, blank=True, null=True)
    emploi = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    date_entree = models.DateField(blank=True, null=True)
