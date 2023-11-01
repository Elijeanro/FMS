from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance,Fournisseur,EtatEngin
from django.contrib.auth.models import User
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.forms.widgets import SelectDateWidget
from django.shortcuts import reverse

    
class PersonneForm(forms.Form):
    nom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Nom'})
    )
    prenom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Prénom'})
    )
    contact = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Contact'})
    )
    grade = forms.ChoiceField(
        choices=[('','Choisir un grade')]+
                [(g.id, g.libelle_grade) for g in Grade.objects.all()]+
                [('create_grade', 'Ajouter un grade')],
        widget=forms.Select(attrs={'class':'form-control mb-3','id':'grade'}),
        required=True
    )
    def clean_grade(self):
        grade_id=self.cleaned_data['grade']
        if grade_id =='create_grade':
            create_url=reverse('create_grade')
            raise forms.ValidationError(create_url)
        return grade_id

    
    def clean_contact(self):
        contact = self.cleaned_data['contact']
        try:
            parsed_number = parse(contact, "TG")
            parsed_number.national_number = int(parsed_number.national_number)
            formatted_number = format_number(parsed_number, PhoneNumberFormat.E164)
            return formatted_number
        except NumberParseException:
            raise forms.ValidationError("Erreur lors de l'analyse du numéro de téléphone.")
        except ValueError:
            raise forms.ValidationError("Numéro de téléphone invalide.")
        
class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        fields = ['nom_marque']
        widgets = {
            'nom_marque': forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nom de la marque'})
        }

class ModeleForm(forms.ModelForm):
    marque = forms.ChoiceField(
        choices=[('','Choisir une marque')]+
                [(m.id, m.nom_marque) for m in Marque.objects.all()]+
                [('create_marque', 'Ajouter une marque')],
        widget=forms.Select(attrs={'class':'form-control mb-3','id':'marque'}),
        required=True
    )
    def clean_marque(self):
        marque_id=self.cleaned_data['marque']
        if marque_id =='create_marque':
            create_url=reverse('create_marque')
            raise forms.ValidationError(create_url)
        return marque_id
    
    annee = forms.DateField(
        widget=SelectDateWidget(years=range(1900, 2101), attrs={'class': 'form-control mb-3'}),
        input_formats=['%Y']
    )
    
    class Meta:
        model = Modele
        fields = ['nom_modele', 'marque', 'annee']
        widgets = {
            'nom_modele': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Nom du modèle'})
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom_fournisseur','adresse','description_fournisseur']
        widgets = {
            'nom_fournisseur':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nom du fournisseur'}),
            'adresse':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Adresse du fournisseur'}),
            'description_fournisseur':forms.Textarea(attrs={'class':'form-control mb-3', 'placeholder':'Donnez une description du fournisseur'}),
        }

class EnginForm(forms.Form):
    immatriculation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Saisir le numéro matricule'}))
    couleur = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': "Donnez la couleur de l'engin"}))
    
    modele_engin = forms.ChoiceField(
        choices=[('', 'Sélectionnez un modèle')] + 
                [(m.id, m.nom_modele) for m in Modele.objects.all()] + 
                [('create_modele', 'Ajouter un modèle')],
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id':'modele'}),
        required=False,
    )
    def clean_modele_engin(self):
        modele_id = self.cleaned_data['modele_engin']
        if modele_id == 'create_modele':
            create_url = reverse('create_modele')  
            raise forms.ValidationError(create_url)
        return modele_id
    
    type_engin = forms.ChoiceField(
        choices=[('', 'Sélectionnez un type d\'engin')] + 
                [(t.id, t.designation) for t in TypeEngin.objects.all()] + 
                [('create_type_engin', 'Ajouter un type d\'engin')],
        widget=forms.Select(attrs={'class': 'form-control mb-3','id':'type_engin'}),
        required=False,
    )
    def clean_type_engin(self):
        type_id = self.cleaned_data['type_engin']
        if type_id == 'create_type_engin':
            create_url = reverse('create_type_engin')  
            raise forms.ValidationError(create_url)
        return type_id
    
    info_engin = forms.ChoiceField(
        choices=[('', 'Informations à propos de cet engin')] + 
                [(i.id, i.info) for i in InfoEngin.objects.all()] + 
                [('create_info_engin', 'Ajouter des informations')],
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id':'info_engin'}),
        required=False,
    )
    def clean_info_engin(self):
        info_id = self.cleaned_data['info_engin']
        if info_id == 'create_info_engin':
            create_url = reverse('create_info_engin')  
            raise forms.ValidationError(create_url)
        return info_id
    
    etat_engin = forms.ChoiceField(
        choices=[('', 'Sélectionnez l\'état de l\'engin')] + 
                [(e.id, e.libelle_etat) for e in EtatEngin.objects.all()] + 
                [('create_etat_engin', 'Ajouter un état')],
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id':'etat_engin'}),
        required=False,
    )
    def clean_etat_engin(self):
        etat_id = self.cleaned_data['etat_engin']
        if etat_id == 'create_etat_engin':
            create_url = reverse('create_etat_engin')  
            raise forms.ValidationError(create_url)
        return etat_id
    
    est_obsolete = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        required=False,
        initial=False,  
    )
    
    fournisseur_engin = forms.ChoiceField(
        choices=[('', 'Sélectionnez le fournisseur de l''engin')] + 
                [(f.id, f.nom_fournisseur) for f in Fournisseur.objects.all()] + 
                [('create_fournisseur', 'Ajouter un fournisseur')],
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id':'fournisseur'}),
        required=False,
    )
    def clean_fournisseur_engin(self):
        fournisseur_id=self.cleaned_data['fournisseur_engin']
        if fournisseur_id == 'create_fournisseur':
            create_url=reverse('create_fournisseur')
            raise forms.ValidationError(create_url)
        return fournisseur_id

    vik = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Valeur initiale du compteur'}),
        required=True
    )
    capa_reserv = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Capacité du réservoir'}),
        required=True
    )
    
class TypeEnginForm(forms.ModelForm):
    class Meta:
        model = TypeEngin
        fields = ['designation','description','nombre_roue']
        widgets = {
            'designation':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Désignation'}),
            'description':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Description'}),
            'nombre_roue':forms.NumberInput(attrs={'class':'form-control mb-3', 'placeholder':'Nombre de roues'}),
        }
class EtatEnginForm(forms.ModelForm):
    class Meta:
        model = EtatEngin
        fields = ['libelle_etat']
        widgets = {
            'libelle_etat':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Etat d''un engin'})
        }

class InfoEnginForm(forms.Form):
    info = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Saisir le libellé d''information'}))
    consommation = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control mb-3', 'placeholder':'Consommation'}))
    vidange = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control mb-3', 'placeholder':'Vidange après combien de kilomètres?'}))
    revision = forms.DurationField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nombre de jours entre deux révisions'}))
    
class RavitaillementCarburantForm(forms.Form):
    cout_rav = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Coût du ravitaillement'}),
        required=True
    )
    engin_rav = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.filter(est_obsolete=False)]+
                [('create_engin', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3','id':'engin'}),
        required=True
    )
    def clean_engin_rav(self):
        engin_id=self.cleaned_data['engin_rav']
        if engin_id == 'create_engin':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id
    
    fournisseur_carburant = forms.ChoiceField(
        choices=[('', 'Sélectionnez le fournisseur de carburant')] + 
                [(f.id, f.nom_fournisseur) for f in Fournisseur.objects.all()] + 
                [('create_fournisseur', 'Ajouter un fournisseur de carburant')],
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id':'fournisseur'}),
        required=False,
    )
    def clean_fournisseur_carburant(self):
        fournisseur_id=self.cleaned_data['fournisseur_carburant']
        if fournisseur_id == 'create_fournisseur':
            create_url=reverse('create_fournisseur')
            raise forms.ValidationError(create_url)
        return fournisseur_id
    
    plein = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
        required=False
    )
    Km_plein = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Kilometrage au plein'}),
        initial=0,
        required=True
    )

class TypeMaintenanceForm(forms.Form):
    libelle_maint = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Libellé de la maintenance'}),
        required=True
    )

class MaintenanceEnginForm(forms.Form):
    type_maint = forms.ChoiceField(
        choices=[('','Selectionner le type de maintenance')]+
                [(t.id, t.libelle_maint) for t in TypeMaintenance.objects.all()]+
                [('create_type_maintenance', 'Ajouter un type de maintenance')],
        widget=forms.Select(attrs={'class':'form-control mb-3','id':'type_maint'}),
        required=True
    )
    def clean_type_maint(self):
        type_maint_id=self.cleaned_data['type_maint']
        if type_maint_id == 'create_type_maintenance':
            create_url=reverse('create_type_maintenance')
            raise forms.ValidationError(create_url)
        return type_maint_id
    
    motif_maint = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Motif de la maintenance'}),
        required=False
    )
    engin_maint = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.all()]+
                [('create_engin', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3','id':'engin'}),
        required=True
    )
    def clean_engin_maint(self):
        engin_id=self.cleaned_data['engin_maint']
        if engin_id == 'create_engin':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id
    
    cout_maint = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Coût de la maintenance'}),
        initial=0,
        required=True
    )
    fournisseur_maint = forms.ChoiceField(
        choices=[('','Selectionner un fournisseur')]+
                [(f.id, f.nom_fournisseur) for f in Fournisseur.objects.all()]+
                [('create_fournisseur', 'Ajouter un fournisseur')],
        widget=forms.Select(attrs={'class':'form-control mb-3', 'id':'fournisseur'}),
        required=False
    )
    def clean_fournisseur_maint(self):
        fournisseur_id=self.cleaned_data['fournisseur_maint']
        if fournisseur_id == 'create_fournisseur':
            create_url=reverse('create_fournisseur')
            raise forms.ValidationError(create_url)
        return fournisseur_id
    
class AttributionForm(forms.Form):
    conducteur = forms.ChoiceField(
        choices=[('','Choisir un conducteur')]+
                [(p.id, p.nom) for p in Personne.objects.filter(grade=5)]+
                [('create_personne', 'Ajouter un conducteur')],
        widget=forms.Select(attrs={'class':'form-control mb-3', 'id':'personne'}),
        required=True
    )
    def clean_conducteur(self):
        conducteur_id=self.cleaned_data['conducteur']
        if conducteur_id == 'create_personne':
            create_url=reverse('create_personne')
            raise forms.ValidationError(create_url)
        return conducteur_id
    
    engin = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.filter(est_obsolete=False)]+
                [('create_engin', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3', 'id':'engin'}),
        required=True
    )
    def clean_engin(self):
        engin_id=self.cleaned_data['engin']
        if engin_id == 'create_engin':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id

class ReleveDistanceForm(forms.Form):
    engin_releve = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.filter(est_obsolete=False)]+
                [('create_engin', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3', 'id':'engin'}),
        required=True
    )
    def clean_engin_releve(self):
        engin_id=self.cleaned_data['engin_releve']
        if engin_id == 'create_engin':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id
    
    nbKmFin = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Kilométrage en fin d''activité de la journée'}),
        required=True
    )
    
    mode_4x4 = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        required=False
    )
    ravitaillement = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        required=False
    )   
    
class T_CardForm(forms.Form):
    
    montant = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Montant'}),
        required=True
    )
    type_engin_tcard = forms.ChoiceField(
        choices=[('','Sélectionner le type d''engin')]+
                [(t.id, t.designation) for t in TypeEngin.objects.all()]+
                [('create_type_engin', 'Ajouter un type d''engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3', 'id':'type_engin'}),
        required=True
    )
    def clean_type_engin_tcard(self):
        type_engin_id=self.cleaned_data['type_engin_tcard']
        if type_engin_id == 'create_type_engin':
            create_url=reverse('create_type_engin')
            raise forms.ValidationError(create_url)
        return type_engin_id