from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Marque(models.Model):
    nom_marque = models.CharField(max_length=40)
    def __str__(self):
        return str(self.nom_marque)
    
class Conducteur(models.Model):
    nom_cond = models.CharField(max_length=25)
    prenom_cond = models.CharField(max_length=50)
    contact_cond = PhoneNumberField(region='TG')
    def __str__(self):
        return f"{self.nom_cond} {self.prenom_cond}"
    
class Modele(models.Model):
    nom_modele = models.CharField(max_length=20)
    marque = models.ForeignKey('Marque', on_delete=models.CASCADE)
    annee = models.SmallIntegerField()
    def __str__(self):
        return f"{self.marque.nom_marque} / {self.nom_modele}"

class Grade(models.Model):
    libelle_grade = models.CharField(max_length=10)
    def __str__(self):
        return str(self.libelle_grade)
    
class Utilisateur(models.Model):
    nom_user = models.CharField(max_length=25)
    prenom_user = models.CharField(max_length=50)
    contact_user = PhoneNumberField(region='TG')
    email_user = models.EmailField()
    motDePasse = models.CharField(max_length=12)
    grade_user = models.ForeignKey('Grade', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nom_user} {self.prenom_user}"
    
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
    def __str__(self):
        return str(self.immatriculation)
  
class RavitaillementCarburant(models.Model):
    date_ravitaillement = models.DateField()
    quantite = models.FloatField()
    engin_rav = models.ForeignKey('Engin',on_delete=models.CASCADE)
    def __str__(self):
        return f"Ravitaillement en carburant du {self.date_ravitaillement}"

class VidangeEngin(models.Model):
    date_vidange = models.DateField()
    engin_vid = models.ForeignKey('Engin',on_delete=models.CASCADE)
    def __str__(self):
        return f"Vidange du {self.date_vidange}"

class TypeMaintenance(models.Model):
    libelle_maintenance = models.CharField(max_length=30)
    def __str__(self):
        return str(self.libelle_maintenance)
    
class MaintenanceEngin(models.Model):
    date_maintenance = models.DateField()
    type_maintenance = models.ForeignKey('TypeMaintenance',on_delete=models.CASCADE)
    motif_maintenance = models.CharField(max_length=120)
    engin_maintenance = models.ForeignKey('Engin',on_delete=models.CASCADE)
    def __str__(self):
        return f"Maintenance du {self.date_maintenance}"
    
class Attribution(models.Model):
    date_attribution = models.DateField()
    conducteur = models.ForeignKey('Conducteur',on_delete=models.CASCADE)
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