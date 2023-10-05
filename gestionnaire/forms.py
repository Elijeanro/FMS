from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,VidangeEngin,\
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
                [('create', 'Ajouter un grade')],
        widget=forms.Select(attrs={'class':'form-control mb-3','id':'id_grade'}),
        required=True
    )
    def clean_grade(self):
        grade_id=self.cleaned_data['grade']
        if grade_id =='create':
            create_url=reverse('administrateur:create_grade')
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
                [('create', 'Ajouter une marque')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    annee = forms.DateField(
        widget=SelectDateWidget(years=range(1900, 2101), attrs={'class': 'form-control mb-3'}),
        input_formats=['%Y']
    )
    def clean_marque(self):
        marque_id=self.cleaned_data['marque']
        if marque_id =='create':
            create_url=reverse('create_marque')
            raise forms.ValidationError(create_url)
        return marque_id
    
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
                [('create', 'Créer un modèle')],
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        required=False,
    )
    
    type_engin = forms.ChoiceField(
        choices=[('', 'Sélectionnez un type d\'engin')] + 
                [(t.id, t.designation) for t in TypeEngin.objects.all()] + 
                [('create', 'Créer un type d\'engin')],
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        required=False,
    )
    
    info_engin = forms.ChoiceField(
        choices=[('', 'Informations à propos de cet engin')] + 
                [(i.id, i.info) for i in InfoEngin.objects.all()] + 
                [('create', 'Créer des informations')],
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        required=False,
    )
    
    etat_engin = forms.ChoiceField(
        choices=[('', 'Sélectionnez l\'état de l\'engin')] + 
                [(e.id, e.libelle_etat) for e in EtatEngin.objects.all()] + 
                [('create', 'Créer un état')],
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        required=False,
    )
    
    est_obsolete = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'display:none'}),
        required=False,
        initial=False,  
    )
    
    fournisseur_engin = forms.ChoiceField(
        choices=[('', 'Sélectionnez le fournisseur de l\'engin')] + 
                [(f.id, f.nom_fournisseur) for f in Fournisseur.objects.all()] + 
                [('create', 'Créer un fournisseur')],
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        required=False,
    )

    def clean_model_engin(self):
        model_id = self.cleaned_data['modele_engin']
        if model_id == 'create':
            create_url = reverse('create_modele')  
            raise forms.ValidationError(create_url)
        return model_id

    def clean_type_engin(self):
        type_id = self.cleaned_data['type_engin']
        if type_id == 'create':
            create_url = reverse('create_type_engin')  
            raise forms.ValidationError(create_url)
        return type_id

    def clean_info_engin(self):
        info_id = self.cleaned_data['info_engin']
        if info_id == 'create':
            create_url = reverse('create_info_engin')  
            raise forms.ValidationError(create_url)
        return info_id

    def clean_etat_engin(self):
        etat_id = self.cleaned_data['etat_engin']
        if etat_id == 'create':
            create_url = reverse('create_etat_engin')  
            raise forms.ValidationError(create_url)
        return etat_id
    
    def clean_fournisseur_engin(self):
        fournisseur_id=self.cleaned_data['fournisseur_engin']
        if fournisseur_id == 'create':
            create_url=reverse('create_fournisseur')
            raise forms.ValidationError(create_url)
        return fournisseur_id
    
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
    quantite_rav = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Quantité de carburant'}),
        initial=0,
        required=True
    )
    cout_rav = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Coût du ravitaillement'}),
        required=True
    )
    engin_rav = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.filter(est_obsolete=False)]+
                [('create', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    fournisseur_carburant = forms.ChoiceField(
        choices=[('', 'Sélectionnez le fournisseur de carburant')] + 
                [(f.id, f.nom_fournisseur) for f in Fournisseur.objects.all()] + 
                [('create', 'Ajouter un fournisseur de carburant')],
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        required=False,
    )
    plein = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    def clean_engin_rav(self):
        engin_id=self.cleaned_data['engin_rav']
        if engin_id == 'create':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id
    
    def clean_fournisseur_carburant(self):
        fournisseur_id=self.cleaned_data['fournisseur_carburant']
        if fournisseur_id == 'create':
            create_url=reverse('create_fournisseur')
            raise forms.ValidationError(create_url)
        return fournisseur_id

class VidangeEnginForm(forms.Form):
    engin_vid = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.filter(est_obsolete=False)]+
                [('create', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    def clean_engin_vid(self):
        engin_id=self.cleaned_data['engin_vid']
        if engin_id == 'create':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id

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
                [('create', 'Ajouter un type de maintenance')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    motif_maint = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Motif de la maintenance'}),
        required=False
    )
    engin_maint = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.all()]+
                [('create', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    cout_maint = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Coût de la maintenance'}),
        initial=0,
        required=True
    )
    fournisseur_maint = forms.ChoiceField(
        choices=[('','Selectionner un fournisseur')]+
                [(f.id, f.nom_fournisseur) for f in Fournisseur.objects.all()]+
                [('create', 'Ajouter un fournisseur')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=False
    )
    def clean_type_maint(self):
        type_maint_id=self.cleaned_data['type_maint']
        if type_maint_id == 'create':
            create_url=reverse('create_type_maintenance')
            raise forms.ValidationError(create_url)
        return type_maint_id
    
    def clean_engin_maint(self):
        engin_id=self.cleaned_data['engin_maint']
        if engin_id == 'create':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id
    
    def clean_fournisseur_maint(self):
        fournisseur_id=self.cleaned_data['fournisseur_maint']
        if fournisseur_id == 'create':
            create_url=reverse('create_fournisseur')
            raise forms.ValidationError(create_url)
        return fournisseur_id

class AttributionForm(forms.Form):
    conducteur = forms.ChoiceField(
        choices=[('','Choisir un conducteur')]+
                [(p.id, p.nom) for p in Personne.objects.filter(grade=5)]+
                [('create', 'Ajouter un conducteur')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    
    engin = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.filter(est_obsolete=False)]+
                [('create', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    
    def clean_conducteur(self):
        conducteur_id=self.cleaned_data['conducteur']
        if conducteur_id == 'create':
            create_url=reverse('create_personne')
            raise forms.ValidationError(create_url)
        return conducteur_id
    
    def clean_engin(self):
        engin_id=self.cleaned_data['engin']
        if engin_id == 'create':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id

class ReleveDistanceForm(forms.Form):
    nbKmDebut = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Kilométrage initial'}),
        required=True
    )
    nbKmFin = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Kilométrage final'}),
        required=True
    )
    engin_releve = forms.ChoiceField(
        choices=[('','Choisir un engin')]+
                [(e.id, e.immatriculation) for e in Engin.objects.filter(est_obsolete=False)]+
                [('create', 'Ajouter un engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        required=True
    )
    
    def clean_engin_releve(self):
        engin_id=self.cleaned_data['engin_releve']
        if engin_id == 'create':
            create_url=reverse('create_engin')
            raise forms.ValidationError(create_url)
        return engin_id