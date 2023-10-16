from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['libelle_grade']
        widgets = {
            'libelle_grade': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Saisir le Grade'})
        }