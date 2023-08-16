from django import forms
from django.forms import DateTimeInput
from gestionnaire.models import TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,VidangeEngin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

    
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
