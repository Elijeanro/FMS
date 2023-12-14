from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class Marque(models.Model):
    nom_marque = models.CharField(max_length=40)
    def __str__(self):
        return str(self.nom_marque)
    
class Modele(models.Model):
    marque = models.ForeignKey('Marque', on_delete=models.CASCADE)
    nom_modele = models.CharField(max_length=20)
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
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    date_creation_personne = models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class Fournisseur(models.Model):
    nom_fournisseur = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)
    description_fournisseur = models.CharField(max_length=255)
    def __str__(self):
        return str(self.nom_fournisseur)
    
class EtatEngin(models.Model):
    libelle_etat = models.CharField(max_length=120)
    def __str__(self):
        return str(self.libelle_etat)
    
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
        return f"Consommation : {self.consommation} L/100Km  | Vidange tous les {self.vidange} Km | Révision tous les {self.revision} jours"
    
class Engin(models.Model):
    immatriculation = models.CharField(max_length=13)
    couleur = models.CharField(max_length=10)
    modele_engin = models.ForeignKey('Modele',on_delete=models.CASCADE)
    type_engin = models.ForeignKey('TypeEngin',on_delete=models.CASCADE)
    info_engin = models.ForeignKey('InfoEngin', on_delete=models.CASCADE)
    etat_engin = models.ForeignKey('EtatEngin', on_delete=models.CASCADE, null=True)
    fournisseur_engin = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    est_obsolete = models.BooleanField(default=False)
    date_creation = models.DateField(default=timezone.now)
    # Nombre de jours d'activités (nja)
    nja = models.IntegerField(default = 0, null = True)
    # valeur initiale du kilometrage
    vik = models.FloatField(null=True)
    # Capacité du réservoir
    capa_reserv = models.FloatField(default=0, null=True)
    has_notification = models.BooleanField(default=False)

    def __str__(self):
        return str(self.immatriculation)
    
class RavitaillementCarburant(models.Model):
    date_rav = models.DateField(auto_now_add=True)
    quantite_rav = models.FloatField(default=0,null=True)
    cout_rav = models.FloatField()
    engin_rav = models.ForeignKey('Engin',on_delete=models.CASCADE)
    fournisseur_carburant = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    carb_dispo = models.FloatField(null=True)
    plein = models.BooleanField(default=False,null=True,blank=True)
    Km_plein = models.FloatField(null=True,blank=True)
    conso = models.FloatField(null=True,blank=True)
    def __str__(self):
        return f"Ravitaillement en carburant du {self.date_rav}"
    def dap(self):
        if self.carb_dispo is not None and self.engin_rav.info_engin is not None and self.engin_rav.info_engin.consommation is not None:
            return (float(self.carb_dispo) * 100 / float(self.engin_rav.info_engin.consommation))
        else:
            return None

    def ecart_conso(self):
        # Récupérez le ravitaillement précédent (basé sur la date de ravitaillement)
        ravitaillement_precedent = RavitaillementCarburant.objects.filter(
            date_rav__lt=self.date_rav, engin_rav=self.engin_rav
        ).order_by('-date_rav').first()

        if ravitaillement_precedent:
            # Il y a un ravitaillement précédent, soustrayez la valeur de Km_plein
            if self.plein :
                ecart = float(self.Km_plein) - float(ravitaillement_precedent.Km_plein)
                return (((float(self.quantite_rav) * 100 / ecart) - self.engin_rav.info_engin.consommation) * 100)
        else:
            # Aucun ravitaillement précédent, renvoyez une valeur par défaut (0 par exemple)
            return 0
    def niveau_carb(self):
        if self.carb_dispo and self.engin_rav.capa_reserv :
            return (float(self.carb_dispo)*100/float(self.engin_rav.capa_reserv))
        else :
            return 0
    def notification_message_ravitaillement(self):
        return f"{self.engin_rav.immatriculation} a besoin de ravitaillement en carburant (niveau : {self.niveau_carb()} %)"

class TypeMaintenance(models.Model):
    libelle_maint = models.CharField(max_length=30)
    def __str__(self):
        return str(self.libelle_maint)
    
class MaintenanceEngin(models.Model):
    date_maint = models.DateField(auto_now_add=True)
    type_maint = models.ForeignKey('TypeMaintenance', on_delete=models.CASCADE, null=True)
    motif_maint = models.CharField(max_length=500, null=True)
    engin_maint = models.ForeignKey('Engin', on_delete=models.CASCADE)
    cout_maint = models.FloatField(default=0)
    fournisseur_maint = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    Km_vid = models.FloatField(default=0)

    def __str__(self):
        return f"Maintenance du {self.date_maint}"

    def reviz(self):
        # Calcul du nombre de jours restants avant la prochaine révision (30 jours par défaut)
        if self.engin_maint.nja is not None:
            return 30 - float(self.engin_maint.nja)
        else:
            return None

    def vid(self):
        if self.type_maint.id == 4:
            # Dans le cas d'une maintenance de type 4, calculez les jours restants avant la prochaine vidange (15 jours par défaut)
            if self.engin_maint.nja is not None:
                return 15 - float(self.engin_maint.nja)
            else:
                return None
        else:
            # Dans d'autres cas, calculez les kilomètres restants avant la prochaine vidange en fonction de la consommation
            if self.engin_maint.info_engin is not None:
                consommation = float(self.engin_maint.info_engin.consommation)
                if consommation > 0:
                    distance_restante = float(self.engin_maint.info_engin.vidange) - float(self.Km_vid)
                    return distance_restante * consommation / 100
                else:
                    return None
            else:
                return None

    def notification_message_maintenance(self):
        if self.engin_maint.type_engin == 2:
            return f"{self.engin_maint.immatriculation} devrait avoir sa vidange dans {self.vid()} jours."
        else : 
            f"{self.engin_maint.immatriculation} devrait avoir sa vidange dans {self.vid()} Km."
        return f"{self.engin_maint.immatriculation} devrait aller en révision dans {self.reviz()} jours."
    
class Attribution(models.Model):
    date_attribution = models.DateField(auto_now_add=True)
    conducteur = models.ForeignKey('Personne',on_delete=models.CASCADE)
    engin = models.ForeignKey('Engin', on_delete=models.CASCADE)
    def __str__(self):
        return f"Attribution du {self.date_attribution}"

class ReleveDistance(models.Model):
    date_releve = models.DateField(auto_now_add=True)
    nbKmDebut = models.FloatField(null=True)
    nbKmFin = models.FloatField(null=True)
    distance = models.FloatField(null=True, default=0)
    engin_releve = models.ForeignKey('Engin', on_delete=models.CASCADE)
    mode_4x4 = models.BooleanField(default=False,null=True)
    carb_depart = models.FloatField(default=0.0,null=True)
    carb_consomme = models.FloatField(default=0.0,null=True)
    carb_restant = models.FloatField(default=0.0,null=True)
    ravitaillement = models.BooleanField(default=False,null=True)
    qte_rav = models.FloatField(null=True)
    date2_rav = models.DateField(null=True)
    def __str__(self):
        return f"Relevé du {self.date_releve}"
    
class T_Card(models.Model):
    date_emploie = models.DateField(auto_now_add=True)
    type_engin_tcard = models.ForeignKey('TypeEngin',on_delete=models.CASCADE,default=1)
    montant = models.FloatField(default=0.0)
    solde = models.FloatField(default=0.0)
    approvisionnement = models.BooleanField(default=False,null=True)
    def __str__(self):
        return f"Carte - {self.type_engin_tcard.designation} | {self.date_emploie}"
    
class ChatBox(models.Model):
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_expediteur')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_destinataire')
    date_d_envoie = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return f"Chat entre {self.expediteur.first_name} & {self.destinataire.first_name} du {self.date_d_envoie}"