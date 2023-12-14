from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance
# from phonenumbers.phonenumberutil import NumberParseException
# from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException
# from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

class PeriodeBilanForm(forms.Form):
    
    date_debut = forms.DateField(
        label='Date de début',
        widget=forms.SelectDateWidget(years=range(2023, 2030))
    )

    date_fin = forms.DateField(
        label='Date de fin',
        widget=forms.SelectDateWidget(years=range(2023, 2030))
    )

    engin = forms.ModelChoiceField(
        label='Engin',
        queryset=Engin.objects.all(),
        empty_label='Sélectionner un engin',
        required=False
    )