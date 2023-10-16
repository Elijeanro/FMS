from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,VidangeEngin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

destinataires=[
    ('Nagode', 'Compagnie Nagode'),
    ('Cheval Blanc', 'Compagnie Cheval Blanc'),
    ('Rakieta', 'Compagnie Rakieta'),
    ('LK', 'Compagnie LK'),
    ('ETRAB', 'Compagnie ETRAB'),
    ('Adji Transport', 'Compagnie Adji Transport'),
    ('DC10', 'Compagnie DC10')
]
class RechercheForm(forms.Form):
    objet = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'placeholder': 'Objet'}, choices=destinataires)
    )
    chaine = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Rechercher'})
    )