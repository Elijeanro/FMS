from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,VidangeEngin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance,Fournisseur,EtatEngin
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.forms.widgets import SelectDateWidget

    
class PersonneForm(forms.Form):
    nom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    prenom = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    contact = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'})
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionnez un grade",
        to_field_name='id'
    )
    
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
            'nom_marque': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nom de la marque'})
        }

class ModeleForm(forms.ModelForm):
    marque = forms.ModelChoiceField(
        queryset=Marque.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choisir la marque'}),
        empty_label=None,
        to_field_name='id'
    )
    annee = forms.DateField(
        widget=SelectDateWidget(years=range(1900, 2101), attrs={'class': 'form-control'}),
        input_formats=['%Y']
    )
    
    class Meta:
        model = Modele
        fields = ['nom_modele', 'marque', 'annee']
        widgets = {
            'nom_modele': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du modèle'})
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom_fournisseur','adresse','description_fournisseur']
        widgets = {
            'nom_fournisseur':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nom du fournisseur'}),
            'adresse':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse du fournisseur'}),
            'description_fournisseur':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Donnez une description du fournisseur'}),
        }

class EnginForm(forms.Form):
    immatriculation=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Saisir le numero matricule'}))
    couleur=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Donnez la couleur de l''engin'}))
    modele_engin=forms.ModelChoiceField(
        queryset=Modele.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionnez un modèle",
        to_field_name='id'
    )
    type_engin=forms.ModelChoiceField(
        queryset=TypeEngin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionnez un type d'engin",
        to_field_name='id'
    )
    info_engin=forms.ModelChoiceField(
        queryset=InfoEngin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Informations à propos de cet engin",
        to_field_name='id'
    )
    etat_engin=forms.ModelChoiceField(
        queryset=EtatEngin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionnez l'état de l'engin",
        to_field_name='id'
    )
    est_obsolete = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    fournisseur_engin=forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionnez le fournisseur de l'engin",
        to_field_name='id'
    )

class TypeEnginForm(forms.ModelForm):
    class Meta:
        model = TypeEngin
        fields = ['designation','description','nombre_roue']
        widgets = {
            'designation':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Désignation'}),
            'description':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}),
            'nombre_roue':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Nombre de roues'}),
        }
class EtatEnginForm(forms.ModelForm):
    class Meta:
        model = EtatEngin
        fields = ['libelle_etat']
        widgets = {
            'libelle_etat':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Etat d''un engin'})
        }

class InfoEnginForm(forms.Form):
    info = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Saisir le libellé d''information'}))
    consommation = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Consommation'}))
    vidange = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Vidange après combien de kilomètres?'}))
    revision = forms.DurationField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de jours entre deux révisions'}))
    
class RavitaillementCarburantForm(forms.Form):
    quantite_rav = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité de carburant'}),
        initial=0,
        required=True
    )
    cout_rav = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Coût du ravitaillement'}),
        required=True
    )
    engin_rav = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un engin'}),
        required=True
    )
    fournisseur_carburant = forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un fournisseur'}),
        required=False
    )
    plein = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )

class VidangeEnginForm(forms.Form):
    engin_vid = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un engin'}),
        required=True
    )

class TypeMaintenanceForm(forms.Form):
    libelle_maint = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Libellé de la maintenance'}),
        required=True
    )

class MaintenanceEnginForm(forms.Form):
    type_maint = forms.ModelChoiceField(
        queryset=TypeMaintenance.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un type de maintenance'}),
        required=True
    )
    motif_maint = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motif de la maintenance'}),
        required=False
    )
    engin_maint = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un engin'}),
        required=True
    )
    cout_maint = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Coût de la maintenance'}),
        initial=0,
        required=True
    )
    fournisseur_maint = forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un fournisseur'}),
        required=False
    )

class AttributionForm(forms.Form):
    conducteur = forms.ModelChoiceField(
        queryset=Personne.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un conducteur'}),
        required=True
    )
    engin = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un engin'}),
        required=True
    )

class ReleveDistanceForm(forms.Form):
    nbKmDebut = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kilométrage initial'}),
        required=True
    )
    nbKmFin = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kilométrage final'}),
        required=True
    )
    engin_releve = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un engin'}),
        required=True
    )
