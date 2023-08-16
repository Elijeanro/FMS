from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Marque(models.Model):
    nom_marque = models.CharField(max_length=40)
    def __str__(self):
        return str(self.nom_marque)
    
class Modele(models.Model):
    nom_modele = models.CharField(max_length=20)
    marque = models.ForeignKey('Marque', on_delete=models.CASCADE)
    annee = models.SmallIntegerField()
    def __str__(self):
        return f"{self.marque.nom_marque} / {self.nom_modele}"

class Grade(models.Model):
    libelle_grade = models.CharField(max_length=50)
    def __str__(self):
        return str(self.libelle_grade)

class Personne(models.Model):
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=50)
    contact = PhoneNumberField(region='TG')
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class Fournisseur(models.Model):
    nom_fournisseur = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)
    description_fournisseur = models.CharField(max_length=255)
    def __str__(self):
        return str(self.nom_fournisseur)
    
class TypeEngin(models.Model):
    designation = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    nombre_roue = models.IntegerField()
    def __str__(self):
        return str(self.designation)

class InfoEngin(models.Model):
    info = models.CharField(max_length=30)
    consommation = models.FloatField()
    vidange = models.FloatField()
    revision = models.DurationField()
    def __str__(self):
        return str(self.info)
    
class Engin(models.Model):
    immatriculation = models.CharField(max_length=13)
    couleur = models.CharField(max_length=10)
    modele_engin = models.ForeignKey('Modele',on_delete=models.CASCADE)
    type_engin = models.ForeignKey('TypeEngin',on_delete=models.CASCADE)
    info_engin = models.ForeignKey('InfoEngin', on_delete=models.CASCADE)
    fournisseur_engin = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.immatriculation)
  
class RavitaillementCarburant(models.Model):
    date_rav = models.DateField()
    quantite_rav = models.FloatField(default=0)
    cout_rav = models.FloatField()
    engin_rav = models.ForeignKey('Engin',on_delete=models.CASCADE)
    fournisseur_carburant = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"Ravitaillement en carburant du {self.date_ravitaillement}"

class VidangeEngin(models.Model):
    date_vid = models.DateField()
    engin_vid = models.ForeignKey('Engin',on_delete=models.CASCADE)
    def __str__(self):
        return f"Vidange du {self.date_vidange}"

class TypeMaintenance(models.Model):
    libelle_maint = models.CharField(max_length=30)
    def __str__(self):
        return str(self.libelle_maint)
    
class MaintenanceEngin(models.Model):
    date_maint = models.DateField()
    type_maint = models.ForeignKey('TypeMaintenance',on_delete=models.CASCADE)
    motif_maint = models.CharField(max_length=120, null=True)
    engin_maint = models.ForeignKey('Engin',on_delete=models.CASCADE)
    cout_maint = models.FloatField(default=0)
    fournisseur_maint = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"Maintenance du {self.date_maint}"
    
class Attribution(models.Model):
    date_attribution = models.DateField()
    conducteur = models.ForeignKey('Personne',on_delete=models.CASCADE)
    engin = models.ForeignKey('Engin', on_delete=models.CASCADE)
    def __str__(self):
        return f"Attribution du {self.date_attribution}"

class ReleveDistance(models.Model):
    date_releve = models.DateField()
    nbKmDebut = models.FloatField()
    nbKmFin = models.FloatField()
    engin_releve = models.ForeignKey('Engin', on_delete=models.CASCADE)
    def __str__(self):
        return f"Relevé du {self.date_releve}"