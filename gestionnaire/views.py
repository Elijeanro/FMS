from django.shortcuts import render,redirect
from django.urls import reverse
from gestionnaire.models import Utilisateur,TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,VidangeEngin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance

def EspaceDGView(request,id_dg):
    return render(request, 'gestionnaire/espace_dg.html')

def EspaceGestionnaireView(request,id_ges):
    return render(request, 'gestionnaire/espace_ges.html')