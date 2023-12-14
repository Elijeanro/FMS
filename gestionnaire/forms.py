from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,Attribution,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance,Fournisseur,EtatEngin
from django.contrib.auth.models import User
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException
from django.forms.widgets import SelectDateWidget
from django.shortcuts import reverse
import datetime

class NonNegativeFloatField(forms.FloatField):
    def clean(self, value):
        cleaned_data = super().clean(value)
        if cleaned_data >= 0:
            return cleaned_data
        else:
            raise forms.ValidationError("La valeur doit être un nombre positif ou nul.")
       
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
        labels = {
            'nom_marque':'Nom de la marque'
        }

class ModeleForm(forms.ModelForm):
    class Meta:
        model = Modele
        fields = '__all__'
        widgets = {
            'nom_modele':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Saisir le modèle'}),
            'annee':forms.NumberInput(attrs={'class':'form-control mb-3', 'placeholder':'Saisir l\'année'}),
        }
        labels = {
            'nom_modele':'Désignation du modèle',
            'annee':'Année de mise en circulation'
        }
    marque = forms.ModelChoiceField(
        queryset=Marque.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Nom de la marque',
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['marque'].queryset = Marque.objects.all()
        if 'marque' in self.data:
            self.fields['marque'].queryset = Marque.objects.all()
        elif self.instance.pk:
            print(self.instance.marque)
            self.fields['marque'].queryset = Marque.objects.filter(pk=self.instance.marque.pk)
    
    def clean_annee(self):
        cette_annee = datetime.datetime.now().year
        annee = self.cleaned_data.get('annee')

        if annee is None or not 1886 <= annee <= cette_annee:
            raise forms.ValidationError("Valeur incorrecte pour l'année. Veuillez saisir une valeur entre 1886 et l'année en cours.")
        return annee
    
class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom_fournisseur','adresse','description_fournisseur']
        widgets = {
            'nom_fournisseur':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nom du fournisseur'}),
            'adresse':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Adresse du fournisseur'}),
            'description_fournisseur':forms.Textarea(attrs={'class':'form-control mb-3', 'placeholder':'Donnez une description du fournisseur'}),
        }
        labels = {
            'nom_fournisseur':'Nom du fournisseur',
            'adresse':'Adresse du fournisseur',
            'description_fournisseur':'Description des activités du fournisseur'
        }

class EnginForm(forms.ModelForm):
    class Meta:
        model = Engin
        fields = ['immatriculation','couleur','modele_engin','type_engin','info_engin','etat_engin','est_obsolete',\
                  'fournisseur_engin','vik','capa_reserv']
    immatriculation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Saisir le numéro matricule'}),label='Immatriculation de l\'engin')
    couleur = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': "Donnez la couleur de l'engin"}), label='Couleur de l\'engin')
    
    modele_engin = forms.ModelChoiceField(
        queryset=Modele.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        label='Modèle de l\'engin',
        required=False,
    )
    
    type_engin = forms.ModelChoiceField(
        queryset=TypeEngin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        label='Type d\'engin',
        required=False,
    )
    
    info_engin = forms.ModelChoiceField(
        queryset=InfoEngin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        label='Informations sur l\'engin',
        required=False,
    )
    
    etat_engin = forms.ModelChoiceField(
        queryset=EtatEngin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id':'etat_engin'}),
        label='Etat de l\'engin',
        required=False,
    )
    
    est_obsolete = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        label='L\'engin est-il obsolète ? ',
        required=False,
        initial=False,  
    )
    
    fournisseur_engin = forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id':'fournisseur'}),
        label='Fournisseur de l\'engin',
        required=False,
    )
    
    vik = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Valeur initiale du compteur'}),
        label='Valeur initiale du compteur de kilométrage',
        required=True
    )
    capa_reserv = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Capacité du réservoir'}),
        label='Capacité du réservoir',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['modele_engin'].queryset = Modele.objects.all()
        if 'modele_engin' in self.data:
            self.fields['modele_engin'].queryset = Modele.objects.all()
        elif self.instance.pk:
            self.fields['modele_engin'].queryset = Modele.objects.filter(pk=self.instance.modele_engin.pk)

        self.fields['type_engin'].queryset = TypeEngin.objects.all()
        if 'type_engin' in self.data:
            self.fields['type_engin'].queryset = TypeEngin.objects.all()
        elif self.instance.pk:
            self.fields['type_engin'].queryset = TypeEngin.objects.filter(pk=self.instance.type_engin.pk)

        self.fields['info_engin'].queryset = InfoEngin.objects.all()
        if 'info_engin' in self.data:
            self.fields['info_engin'].queryset = InfoEngin.objects.all()
        elif self.instance.pk:
            self.fields['info_engin'].queryset = InfoEngin.objects.filter(pk=self.instance.info_engin.pk)

        self.fields['etat_engin'].queryset = EtatEngin.objects.all()
        if 'etat_engin' in self.data:
            self.fields['etat_engin'].queryset = EtatEngin.objects.all()
        elif self.instance.pk:
            self.fields['etat_engin'].queryset = EtatEngin.objects.filter(pk=self.instance.etat_engin.pk)

        self.fields['fournisseur_engin'].queryset = Fournisseur.objects.all()
        if 'fournisseur_engin' in self.data:
            self.fields['fournisseur_engin'].queryset = Fournisseur.objects.all()
        elif self.instance.pk:
            self.fields['fournisseur_engin'].queryset = Fournisseur.objects.filter(pk=self.instance.fournisseur_engin.pk)
    
class TypeEnginForm(forms.ModelForm):
    class Meta:
        model = TypeEngin
        fields = ['designation','description','nombre_roue']
        widgets = {
            'designation':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Désignation'}),
            'description':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Description'}),
            'nombre_roue':forms.NumberInput(attrs={'class':'form-control mb-3', 'placeholder':'Nombre de roues'}),
        }
        labels = {
            'designation':'Désignation du type d\'engin',
            'description':'Description du type d\'engin',
            'nombre_roue':'Nombre de roue'
        }

class EtatEnginForm(forms.ModelForm):
    class Meta:
        model = EtatEngin
        fields = ['libelle_etat']
        widgets = {
            'libelle_etat':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Etat d''un engin'})
        }
        labels = {
            'libelle_etat':'Libellé de l''état de l\'engin'
        }

class InfoEnginForm(forms.Form):
    info = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Saisir le libellé d''information'}),label='Titre de l''information')
    consommation = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control mb-3', 'placeholder':'Consommation'}),label='Consommation')
    vidange = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control mb-3', 'placeholder':'Vidange après combien de kilomètres?'}),label='La vidange doit être faite au bout de combien de kilomètres ? ')
    revision = forms.DurationField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nombre de jours entre deux révisions'}),label='La révision doit être faite après combien de jours d\'activités ? ')
    
class RavitaillementCarburantForm(forms.ModelForm):
    class Meta:
        model = RavitaillementCarburant
        fields = ['cout_rav','engin_rav','fournisseur_carburant','plein','Km_plein']
    cout_rav = NonNegativeFloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Coût du ravitaillement', 'min': 700 }),
        label='Coût du ravitaillement en F CFA',
        required=True
    )
    engin_rav = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class':'form-control mb-3'}),
        label='Engin ravitaillé',
        required=True
    )
    
    fournisseur_carburant = forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        label='Fournisseur du carburant',
        required=False,
    )

    plein = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
        label='Etait-ce le plein ? ',
        required=False
    )
    Km_plein = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Kilometrage au plein'}),
        initial=0,
        label='Valeur du kilométrage au plein (en Km)',
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['engin_rav'].queryset = Engin.objects.none()
        if 'engin_rav' in self.data:
            self.fields['engin_rav'].queryset = Engin.objects.all()
        elif self.instance.pk:
            self.fields['engin_rav'].queryset = Engin.objects.filter(pk=self.instance.engin_rav.pk)

        self.fields['fournisseur_carburant'].queryset = Fournisseur.objects.none()
        if 'fournisseur_carburant' in self.data:
            self.fields['fournisseur_carburant'].queryset = Fournisseur.objects.all()
        elif self.instance.pk:
            self.fields['fournisseur_carburant'].queryset = Fournisseur.objects.filter(pk=self.instance.fournisseur_carburant.pk)
    
    def clean_cout_rav(self):
        cout_rav = self.cleaned_data['cout_rav']
        if cout_rav < 700:
            raise forms.ValidationError("Montant invalide car inférieur à 700 F CFA.")
        return cout_rav
    
class TypeMaintenanceForm(forms.Form):
    libelle_maint = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Libellé de la maintenance'}),
        label='Libellé du type de maintenance',
        required=True
    )

class MaintenanceEnginForm(forms.ModelForm):
    class Meta:
        model = MaintenanceEngin
        fields = ['type_maint','motif_maint','engin_maint','cout_maint','fournisseur_maint']
     
    type_maint = forms.ModelChoiceField(
        queryset=TypeMaintenance.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Type de maintenance',
        required=True
    )

    motif_maint = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Motif de la maintenance'}),
        label='Motif de la maintenance',
        required=False
    )
    engin_maint = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Engin concerné',
        required=True
    )
    
    cout_maint = forms.FloatField(
        widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Coût de la maintenance'}),
        initial=0,
        label='Coût de la maintenance en F CFA',
        required=True
    )
    fournisseur_maint = forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Fournisseur de la maintenance',
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['engin_maint'].queryset = Engin.objects.all()
        if 'engin_maint' in self.data:
            self.fields['engin_maint'].queryset = Engin.objects.all()
        elif self.instance.pk:
            self.fields['engin_maint'].queryset = Engin.objects.filter(pk=self.instance.engin_maint.pk)


        self.fields['fournisseur_maint'].queryset = Fournisseur.objects.none()
        if 'fournisseur_maint' in self.data:
            self.fields['fournisseur_maint'].queryset = Fournisseur.objects.all()
        elif self.instance.pk:
            self.fields['fournisseur_maint'].queryset = Fournisseur.objects.filter(pk=self.instance.fournisseur_maint.pk)

    def clean_cout_maint(self):
        cout_maint = self.cleaned_data['cout_maint']
        if cout_maint < 100:
            raise forms.ValidationError("Montant invalide car inférieur à 100 F CFA.")
        return cout_maint
    
class AttributionForm(forms.ModelForm):
    class Meta:
        model = Attribution
        fields = ['conducteur','engin']
    
    conducteur = forms.ModelChoiceField(
        queryset=Personne.objects.filter(grade=5),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Nom du conducteur',
        required=True
    )

    engin = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Immatriculation de l\'engin',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['engin'].queryset = Engin.objects.all()
        if 'engin' in self.data:
            self.fields['engin'].queryset = Engin.objects.all()
        elif self.instance.pk:
            self.fields['engin'].queryset = Engin.objects.filter(pk=self.instance.engin.pk)

        self.fields['conducteur'].queryset = Personne.objects.all()
        if 'conducteur' in self.data:
            self.fields['conducteur'].queryset = Personne.objects.all()
        elif self.instance.pk:
            self.fields['conducteur'].queryset = Personne.objects.filter(pk=self.instance.conducteur.pk)
    
class ReleveDistanceForm(forms.ModelForm):
    class Meta:
        model = ReleveDistance
        fields = ['engin_releve','nbKmFin','mode_4x4','ravitaillement']
        widgets = {
           'mode_4x4' : forms.CheckboxInput(),
           'ravitaillement' : forms.CheckboxInput(), 
        }
        labels = {
            'mode_4x4' : 'Le mode 4x4 activé ',
            'ravitaillement' : 'Engin ravitaillé dans la journée ',
        }

    engin_releve = forms.ModelChoiceField(
        queryset=Engin.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Engin concerné',
        required=True
    )

    nbKmFin = forms.FloatField(
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        label='Valeur du kilométrage en fin de journée (en Km)',
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['engin_releve'].queryset = Engin.objects.none()
        if 'engin_releve' in self.data:
            self.fields['engin_releve'].queryset = Engin.objects.all()
        elif self.instance.pk:
            self.fields['engin_releve'].queryset = Engin.objects.filter(pk=self.instance.engin_releve.pk)
    
    def clean_nbKmFin(self):
        engin_releve = self.cleaned_data.get('engin_releve')
        valeur = ReleveDistance.objects.filter(
            engin_releve=engin_releve
        ).exclude(id=self.instance.id if self.instance else 0).last()
        nbKmFin = self.cleaned_data['nbKmFin']
        if nbKmFin < 0:
            raise forms.ValidationError("Le kilométrage en fin de journée ne peut pas être négatif.")
        elif nbKmFin < float(valeur.nbKmFin) :
            raise forms.ValidationError("La valeur du Kilométrage en fin de la journée en cours ne doit pas être inférieure à {} Km. Veuillez corriger".format(float(valeur.nbKmFin)))
        return nbKmFin
        
class T_CardForm(forms.Form):
    
    montant = NonNegativeFloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Montant'}),
        label='Montant approvisionné',
        required=True
    )
    type_engin_tcard = forms.ChoiceField(
        choices=[('','Sélectionner le type d\'engin')]+
                [(t.id, t.designation) for t in TypeEngin.objects.all()]+
                [('create_type_engin', 'Ajouter un type d\'engin')],
        widget=forms.Select(attrs={'class':'form-control mb-3', 'id':'type_engin'}),
        label='Type d\'engin concerné par la carte',
        required=True
    )
    def clean_type_engin_tcard(self):
        type_engin_id=self.cleaned_data['type_engin_tcard']
        if type_engin_id == 'create_type_engin':
            create_url=reverse('create_type_engin')
            raise forms.ValidationError(create_url)
        return type_engin_id
    