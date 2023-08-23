from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import (
    Marque, Modele, Fournisseur, TypeEngin, EtatEngin,Engin, TypeMaintenance, Fournisseur, Personne,
    InfoEngin, RavitaillementCarburant,Grade,VidangeEngin,MaintenanceEngin,ReleveDistance,Attribution
)
from .forms import (
    InfoEnginForm, RavitaillementCarburantForm, VidangeEnginForm,MarqueForm,
    ModeleForm, FournisseurForm, EnginForm, TypeEnginForm, EtatEnginForm,PersonneForm,
    TypeMaintenanceForm, MaintenanceEnginForm, AttributionForm, ReleveDistanceForm
)

def creation(request,sujet):
    context={}
    context['sujet']=sujet
    return render(request,'gestionnaire/creation.html',context)

def delete(request,sujet):
    context={}
    context['sujet']=sujet
    return render(request,'gestionnaire/delete.html',context)

def details(request,pk,sujet):
    context={}
    context['pk']=pk
    objet=None
    if sujet=='personne':
        objet=get_object_or_404(Personne, pk=pk)
    elif sujet=='marque':
        objet=get_object_or_404(Marque, pk=pk)
    elif sujet=='modele':
        objet=get_object_or_404(Modele, pk=pk)
    elif sujet=='fournisseur':
        objet=get_object_or_404(Fournisseur, pk=pk)
    elif sujet=='engin':
        objet=get_object_or_404(Engin, pk=pk)
    elif sujet=='type_engin':
        objet=get_object_or_404(TypeEngin, pk=pk)
    elif sujet=='etat_engin':
        objet=get_object_or_404(EtatEngin, pk=pk)
    elif sujet=='info_engin':
        objet=get_object_or_404(InfoEngin, pk=pk)
    elif sujet=='ravitaillement_engin':
        objet=get_object_or_404(RavitaillementCarburant, pk=pk)
    elif sujet=='vidange_engin':
        objet=get_object_or_404(VidangeEngin, pk=pk)
    elif sujet=='type_maintenance':
        objet=get_object_or_404(TypeMaintenance, pk=pk)
    elif sujet=='maintenance_engin':
        objet=get_object_or_404(MaintenanceEngin, pk=pk)
    elif sujet=='attribution':
        objet=get_object_or_404(Attribution, pk=pk)
    elif sujet=='releve_distance':
        objet=get_object_or_404(ReleveDistance, pk=pk)
    context['objet']=objet
    return render(request,'gestionnaire/details.html',context)

def lists(request,sujet):
    context={}
    context['sujet']=sujet
    objet=None
    if sujet=='personne':
        objet=Personne.objects.all()
    elif sujet=='marque':
        objet=Marque.objects.all()
    elif sujet=='modele':
        objet=Modele.objects.all()
    elif sujet=='fournisseur':
        objet=Fournisseur.objects.all()
    elif sujet=='engin':
        objet=Engin.objects.all()
    elif sujet=='type_engin':
        objet=TypeEngin.objects.all()
    elif sujet=='etat_engin':
        objet=EtatEngin.objects.all()
    elif sujet=='info_engin':
        objet=InfoEngin.objects.all()
    elif sujet=='ravitaillement_engin':
        objet=RavitaillementCarburant.objects.all()
    elif sujet=='vidange_engin':
        objet=VidangeEngin.objects.all()
    elif sujet=='type_maintenance':
        objet=TypeMaintenance.objects.all()
    elif sujet=='maintenance_engin':
        objet=MaintenanceEngin.objects.all()
    elif sujet=='attribution':
        objet=Attribution.objects.all()
    elif sujet=='releve_distance':
        objet=ReleveDistance.objects.all()
    context['objet']=objet
    return render(request,'gestionnaire/lists.html',context)

def results(request,sujet):
    context={}
    context['sujet']=sujet
    return render(request,'gestionnaire/results.html',context)

def update(request,sujet):
    context={}
    context['sujet']=sujet
    return render(request,'gestionnaire/update.html',context)

"""
LES CREATE
"""
def create_personne(request):
    sujet='personne'
    if request.method == "POST":
        form=PersonneForm(request.POST)
        if form.is_valid():
            donnees=form.cleaned_data
            nom=donnees['nom']
            prenom=donnees['prenom']
            contact=donnees['contact']
            grade=Grade.objects.get(id=5)
            personne=Personne.objects.filter(nom=nom,prenom=prenom,contact=contact,grade=grade)
            if personne is not None:
                messages.info(request,"Cette personne existe déjà ! ")
            else:
                personne.save()
                pk=personne.id
                messages.info(request,"Succès d'enrégistrement ! ")
                return redirect(reverse('gestionnaire:details',args=[sujet]))
    else:
        form=PersonneForm()
    return render(request,'gestionnaire/creation.html',{'form':form,'sujet':sujet})        

def create_marque(request):
    sujet = 'marque'
    
    if request.method == "POST":
        form = MarqueForm(request.POST)
        if form.is_valid():
            nom_marque = form.cleaned_data['nom_marque']
            
            existing_marque = Marque.objects.filter(nom_marque=nom_marque).first()
            if existing_marque:
                messages.error(request, 'Une marque avec ce nom existe déjà.')
            else:
                form.save()
                pk=Marque.objects.filter(nom_marque=nom_marque).values('id')
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = MarqueForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})


def create_modele(request):
    sujet = 'modele'
    
    if request.method == "POST":
        form = ModeleForm(request.POST)
        if form.is_valid():
            nom_modele = form.cleaned_data['nom_modele']
            marque = form.cleaned_data['marque']
            
            # Vérifier si un modèle avec le même nom et la même marque existe déjà
            existing_modele = Modele.objects.filter(nom_modele=nom_modele, marque=marque).first()
            if existing_modele:
                # Modèle existe déjà, affichez un message d'erreur ou redirigez selon vos besoins
                messages.error(request, 'Un modèle avec ce nom et cette marque existe déjà.')
            else:
                form.save()
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = ModeleForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})

def create_fournisseur(request):
    sujet = 'fournisseur'
    
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            nom_fournisseur = form.cleaned_data['nom_fournisseur']
            
            # Vérifier si un fournisseur avec le même nom existe déjà
            existing_fournisseur = Fournisseur.objects.filter(nom_fournisseur=nom_fournisseur).first()
            if existing_fournisseur:
                # Fournisseur existe déjà, affichez un message d'erreur ou redirigez selon vos besoins
                messages.error(request, 'Un fournisseur avec ce nom existe déjà.')
            else:
                form.save()
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = FournisseurForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})


def create_engin(request):
    sujet = 'engin'
    
    if request.method == "POST":
        form = EnginForm(request.POST)
        if form.is_valid():
            immatriculation = form.cleaned_data['immatriculation']
            
            # Vérifier si un engin avec le même numéro d'immatriculation existe déjà
            existing_engin = Engin.objects.filter(immatriculation=immatriculation).first()
            if existing_engin:
                # Engin existe déjà, affichez un message d'erreur ou redirigez selon vos besoins
                messages.error(request, 'Un engin avec ce numéro d''immatriculation existe déjà.')
            else:
                form.save()
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = EnginForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})

def create_type_engin(request):
    sujet = 'type_engin'
    
    if request.method == "POST":
        form = TypeEnginForm(request.POST)
        if form.is_valid():
            designation = form.cleaned_data['designation']
            
            # Vérifier si un type d'engin avec le même libellé de désignation existe déjà
            existing_type_engin = TypeEngin.objects.filter(designation=designation).first()
            if existing_type_engin:
                # Type d'engin existe déjà, affichez un message d'erreur ou redirigez selon vos besoins
                messages.error(request, 'Un type d''engin avec ce libellé de désignation existe déjà.')
            else:
                form.save()
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = TypeEnginForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})


def create_etat_engin(request):
    sujet = 'etat_engin'
    
    if request.method == "POST":
        form = EtatEnginForm(request.POST)
        if form.is_valid():
            libelle_etat = form.cleaned_data['libelle_etat']
            
            # Vérifier si un état d'engin avec le même libellé existe déjà
            existing_etat_engin = EtatEngin.objects.filter(libelle_etat=libelle_etat).first()
            if existing_etat_engin:
                # État d'engin existe déjà, affichez un message d'erreur ou redirigez selon vos besoins
                messages.error(request, 'Un état d\'engin avec ce libellé existe déjà.')
            else:
                form.save()
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = EtatEnginForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})


def create_info_engin(request):
    sujet = 'info_engin'
    
    if request.method == "POST":
        form = InfoEnginForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data['info']
            
            # Vérifier si des informations d'engin avec le même libellé existent déjà
            existing_info_engin = InfoEngin.objects.filter(info=info).first()
            if existing_info_engin:
                # Informations d'engin existent déjà, affichez un message d'erreur ou redirigez selon vos besoins
                messages.error(request, 'Des informations d\'engin avec ce libellé existent déjà.')
            else:
                form.save()
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = InfoEnginForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})

def create_ravitaillement_carburant(request):
    sujet='ravitaillement_carburant'
    if request.method == "POST":
        form = RavitaillementCarburantForm(request.POST)
        if form.is_valid():
            
            return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = RavitaillementCarburantForm()
    return render(request,'gestionnaire/creation.html',{'form':form,'sujet':sujet})

def create_vidange_engin(request):
    sujet='vidange_engin'
    if request.method == "POST":
        form = VidangeEnginForm(request.POST)
        if form.is_valid():
            
            return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = VidangeEnginForm()
    return render(request,'gestionnaire/creation.html',{'form':form,'sujet':sujet})

def create_type_maintenance(request):
    sujet = 'type_maintenance'
    
    if request.method == "POST":
        form = TypeMaintenanceForm(request.POST)
        if form.is_valid():
            libelle_maint = form.cleaned_data['libelle_maint']
            
            # Vérifier si un type de maintenance avec le même libellé existe déjà
            existing_type_maintenance = TypeMaintenance.objects.filter(libelle_maint=libelle_maint).first()
            if existing_type_maintenance:
                # Type de maintenance existe déjà, affichez un message d'erreur ou redirigez selon vos besoins
                messages.error(request, 'Un type de maintenance avec ce libellé existe déjà.')
            else:
                form.save()
                return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = TypeMaintenanceForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})


def create_maintenance_engin(request):
    sujet='maintenance_engin'
    if request.method == "POST":
        form = MaintenanceEnginForm(request.POST)
        if form.is_valid():
            
            return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = MaintenanceEnginForm()
    return render(request,'gestionnaire/creation.html',{'form':form,'sujet':sujet})

def create_attribution(request):
    sujet='attribution'
    if request.method == "POST":
        form = AttributionForm(request.POST)
        if form.is_valid():
            
            return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = AttributionForm()
    return render(request,'gestionnaire/creation.html',{'form':form,'sujet':sujet})

def create_releve_distance(request):
    sujet='releve_distance'
    if request.method == "POST":
        form = ReleveDistanceForm(request.POST)
        if form.is_valid():
            return redirect(reverse('gestionnaire:details',args=[sujet]))  
    else:
        form = ReleveDistanceForm()
    return render(request,'gestionnaire/creation.html',{'form':form,'sujet':sujet})

"""
LES UPDATES
"""  
def update_personne(request, pk):
    sujet='personne'
    personne = get_object_or_404(Personne, pk=pk)
    if request.method == 'POST':
        form = PersonneForm(request.POST, instance=personne)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = PersonneForm(instance=personne)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_type_engin(request, pk):
    sujet='type_engin'
    type_engin = get_object_or_404(TypeEngin, pk=pk)
    if request.method == 'POST':
        form = TypeEnginForm(request.POST, instance=type_engin)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = TypeEnginForm(instance=type_engin)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_modele(request, pk):
    sujet='modele'
    modele = get_object_or_404(Modele, pk=pk)
    if request.method == 'POST':
        form = ModeleForm(request.POST, instance=modele)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = ModeleForm(instance=modele)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_fournisseur(request, pk):
    sujet='fournisseur'
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_info_engin(request, pk):
    sujet='info_engin'
    info = get_object_or_404(InfoEngin, pk=pk)
    if request.method == 'POST':
        form = InfoEnginForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = InfoEnginForm(instance=info)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_ravitaillement_carburant(request, pk):
    sujet='ravitaillement_carburant'
    ravitaillement = get_object_or_404(RavitaillementCarburant, pk=pk)
    if request.method == 'POST':
        form = RavitaillementCarburantForm(request.POST, instance=ravitaillement)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = RavitaillementCarburantForm(instance=ravitaillement)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_engin(request, pk):
    sujet='engin'
    engin = get_object_or_404(Engin, pk=pk)
    if request.method == 'POST':
        form = EnginForm(request.POST, instance=engin)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = EnginForm(instance=engin)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_marque(request, pk):
    sujet='marque'
    marque = get_object_or_404(Marque, pk=pk)
    if request.method == 'POST':
        form = MarqueForm(request.POST, instance=marque)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = MarqueForm(instance=marque)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_etat_engin(request, pk):
    sujet='etat_engin'
    etat_engin = get_object_or_404(EtatEngin, pk=pk)
    if request.method == 'POST':
        form = EtatEnginForm(request.POST, instance=etat_engin)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = EtatEnginForm(instance=etat_engin)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_vidange_engin(request, pk):
    sujet='vidange_engin'
    vidange_engin = get_object_or_404(VidangeEngin, pk=pk)
    if request.method == 'POST':
        form = VidangeEnginForm(request.POST, instance=vidange_engin)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = VidangeEnginForm(instance=vidange_engin)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_maintenance_engin(request, pk):
    sujet='maintenance_engin'
    maintenance_engin = get_object_or_404(MaintenanceEngin, pk=pk)
    if request.method == 'POST':
        form = MaintenanceEnginForm(request.POST, instance=maintenance_engin)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = MaintenanceEnginForm(instance=maintenance_engin)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_type_maintenance(request, pk):
    sujet='type_maintenance'
    type_maintenance = get_object_or_404(TypeMaintenance, pk=pk)
    if request.method == 'POST':
        form = TypeMaintenanceForm(request.POST, instance=type_maintenance)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = TypeMaintenanceForm(instance=type_maintenance)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_attribution(request, pk):
    sujet='attribution'
    attribution = get_object_or_404(Attribution, pk=pk)
    if request.method == 'POST':
        form = AttributionForm(request.POST, instance=attribution)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = AttributionForm(instance=attribution)
    return render(request, 'gestionnaire/update.html', {'form': form})

def update_releve_distance(request, pk):
    sujet='releve_distance'
    releve_distance = get_object_or_404(ReleveDistance, pk=pk)
    if request.method == 'POST':
        form = ReleveDistanceForm(request.POST, instance=releve_distance)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestionnaire:details', args=[sujet]))  
    else:
        form = ReleveDistanceForm(instance=releve_distance)
    return render(request, 'gestionnaire/update.html', {'form': form})

"""
LES DELETE
"""

def delete_modele(request, modele_id):
    sujet='modele'
    modele = get_object_or_404(Modele, pk=modele_id)
    if request.method == 'POST':
        modele.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))  
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'modele'})

def delete_info_engin(request, info_engin_id):
    sujet='info_engin'
    info_engin = get_object_or_404(InfoEngin, pk=info_engin_id)
    
    if request.method == 'POST':
        info_engin.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'info_engin'})

def delete_ravitaillement_carburant(request, ravitaillement_carburant_id):
    sujet='ravitaillement_carburant'
    ravitaillement_carburant = get_object_or_404(RavitaillementCarburant, pk=ravitaillement_carburant_id)
    
    if request.method == 'POST':
        ravitaillement_carburant.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'ravitaillement_carburant'})

def delete_personne(request, personne_id):
    sujet='personne'
    personne = get_object_or_404(Personne, pk=personne_id)
    
    if request.method == 'POST':
        personne.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'personne'})

def delete_marque(request, marque_id):
    sujet='marque'
    marque = get_object_or_404(Marque, pk=marque_id)
    
    if request.method == 'POST':
        marque.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'marque'})

def delete_fournisseur(request, fournisseur_id):
    sujet='fournisseur'
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    
    if request.method == 'POST':
        fournisseur.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'fournisseur'})

def delete_engin(request, engin_id):
    sujet='engin'
    engin = get_object_or_404(Engin, pk=engin_id)
    
    if request.method == 'POST':
        engin.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'engin'})

def delete_type_engin(request, type_engin_id):
    sujet='type_engin'
    type_engin = get_object_or_404(TypeEngin, pk=type_engin_id)
    
    if request.method == 'POST':
        type_engin.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'type_engin'})

def delete_etat_engin(request, etat_engin_id):
    sujet='etat_engin'
    etat_engin = get_object_or_404(EtatEngin, pk=etat_engin_id)
    
    if request.method == 'POST':
        etat_engin.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'etat_engin'})

def delete_vidange_engin(request, vidange_engin_id):
    sujet='vidange_engin'
    vidange_engin = get_object_or_404(VidangeEngin, pk=vidange_engin_id)
    
    if request.method == 'POST':
        vidange_engin.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'vidange_engin'})

def delete_type_maintenance(request, type_maintenance_id):
    sujet='type_maintenance'
    type_maintenance = get_object_or_404(TypeMaintenance, pk=type_maintenance_id)
    
    if request.method == 'POST':
        type_maintenance.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'type_maintenance'})

def delete_maintenance_engin(request, maintenance_engin_id):
    sujet='maintenance_engin'
    maintenance_engin = get_object_or_404(MaintenanceEngin, pk=maintenance_engin_id)
    
    if request.method == 'POST':
        maintenance_engin.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'maintenance_engin'})

def delete_attribution(request, attribution_id):
    sujet='attribution'
    attribution = get_object_or_404(Attribution, pk=attribution_id)
    
    if request.method == 'POST':
        attribution.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'attribution'})

def delete_releve_distance(request, releve_distance_id):
    sujet='releve_distance'
    releve_distance = get_object_or_404(ReleveDistance, pk=releve_distance_id)
    
    if request.method == 'POST':
        releve_distance.delete()
        return redirect(reverse('gestionnaire:lists', args=[sujet]))
    
    return render(request, 'gestionnaire/delete.html', {'sujet': 'releve_distance'})
