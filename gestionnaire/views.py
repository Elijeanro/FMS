from wsgiref.simple_server import WSGIRequestHandler
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Max
import datetime
from django.http import HttpRequest, JsonResponse

from .models import (
    Marque, Modele, Fournisseur, TypeEngin, EtatEngin,Engin, TypeMaintenance, Fournisseur, Personne,
    InfoEngin, RavitaillementCarburant,Grade,MaintenanceEngin,ReleveDistance,Attribution,T_Card
)
from .forms import (
    InfoEnginForm, RavitaillementCarburantForm,MarqueForm,
    ModeleForm, FournisseurForm, EnginForm, TypeEnginForm, EtatEnginForm,PersonneForm,
    TypeMaintenanceForm, MaintenanceEnginForm, AttributionForm, ReleveDistanceForm, T_CardForm
)
from django.contrib.auth.decorators import login_required

@login_required
def creation(request,sujet):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        context={
            'sujet':sujet,
            'grade_id':grade_id,
            'personne':personne,
        }

        return render(request,'gestionnaire/creation.html',context)
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})
    
def delete(request,sujet):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id) 
        
        context={
            'sujet':sujet,
            'grade_id':grade_id,
            'personne':personne,
        }
        return render(request,'gestionnaire/delete.html',context)
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})   

@login_required
def details(request, pk, sujet):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id) 
        
        context = {'pk': pk}
        context['sujet']=sujet
        context['grade_id'] = grade_id
        context['personne'] =personne
        sujet_to_model = {
            'utilisateur':User,
            'personne': Personne,
            'marque': Marque,
            'modele': Modele,
            'fournisseur': Fournisseur,
            'engin': Engin,
            'type_engin': TypeEngin,
            'etat_engin': EtatEngin,
            'info_engin': InfoEngin,
            'ravitaillement_carburant': RavitaillementCarburant,
            'type_maintenance': TypeMaintenance,
            'maintenance_engin': MaintenanceEngin,
            'attribution': Attribution,
            'releve_distance': ReleveDistance,
            't_card': T_Card,
        }
        
        if sujet in sujet_to_model:
            objet = get_object_or_404(sujet_to_model[sujet], pk=pk)
            
            if sujet == 'releve_distance':
                distance = float(objet.nbKmFin) - float(objet.nbKmDebut)
                context['distance'] = distance
        else:
            objet = None
            
        print("objet:", objet)

        context['objet'] = objet
        return render(request, 'gestionnaire/details.html', context)
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})
    
@login_required
def lists(request, sujet):
   
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        context={
            'sujet':sujet,
            'grade_id':grade_id,
            'personne':personne,
        }
        sujet_to_model = {
            'utilisateur':User,
            'personne': Personne,
            'marque': Marque,
            'modele': Modele,
            'fournisseur': Fournisseur,
            'engin': Engin,
            'type_engin': TypeEngin,
            'etat_engin': EtatEngin,
            'info_engin': InfoEngin,
            'ravitaillement_carburant': RavitaillementCarburant,
            'type_maintenance': TypeMaintenance,
            'maintenance_engin': MaintenanceEngin,
            'attribution': Attribution,
            'releve_distance': ReleveDistance,
            't_card':T_Card,
        }

        if sujet in sujet_to_model:
            objet = sujet_to_model[sujet].objects.all()
        else:
            objet = None

        context['objet'] = objet
        return render(request, 'gestionnaire/lists.html', context)
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

@login_required
def results(request,sujet):
   
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        context={
            'sujet':sujet,
            'grade_id':grade_id,
            'personne':personne,
        }
        return render(request,'gestionnaire/results.html',context)

    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

@login_required    
def update(request,sujet):
   
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        context={
            'sujet':sujet,
            'grade_id':grade_id,
            'personne':personne,
        }
        return render(request,'gestionnaire/update.html',context)
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})
    
@login_required
def update_notifications(engin_id):
    # Mise à jour du champ has_notification lors de la sauvegarde
    ravitaillement_notifications = RavitaillementCarburant.objects.filter(engin_rav=engin_id).order_by('-date_rav').first()
    maint = MaintenanceEngin.objects.filter(engin_maint=engin_id).order_by('-date_maint').first()
    engin = Engin.objects.get(id=engin_id)
    maintenance_notifications = None  # Déclarer la variable en dehors des conditions

    if maint is not None:
        if maint.type_maint == 4 and maint.vid() <= 15:
            maintenance_notifications = maint
        elif maint.type_maint in range(1, 4) and maint.reviz() <= 30:
            maintenance_notifications = maint

    if ravitaillement_notifications is not None and ravitaillement_notifications.niveau_carb() <= 15:
        engin.has_notification = True

    if maintenance_notifications is not None:
        engin.has_notification = True

    engin.save()

"""
LES CREATE
"""

@login_required
def create_personne(request):
   
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
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
                    return redirect(reverse('gestionnaire:details',args=[pk, sujet]))
        else:
            form=PersonneForm()
        return render(request,'gestionnaire/creation.html',{'form':form, 
                                                            'sujet':sujet,
                                                            'personne':personne, 
                                                            'grade_id':grade_id, 
                                                            'grade':grade})        

    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

@login_required    
def create_marque(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'La marque'
        
        if request.method == "POST":
            form = MarqueForm(request.POST)
            if form.is_valid():
                nom_marque = form.cleaned_data['nom_marque']
                
                existing_marque = Marque.objects.filter(nom_marque=nom_marque).first()
                if existing_marque:
                    messages.error(request, 'Une marque avec ce nom existe déjà.')
                else:
                    marque = Marque(
                        nom_marque=nom_marque,
                    )
                    marque.save() 
                    return redirect(reverse('gestionnaire:details', args=[marque.id, sujet]))  
        else:
            form = MarqueForm()
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet,
                                                              'personne':personne, 
                                                              'grade_id':grade_id, 
                                                              'grade':grade})
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

@login_required
def create_modele(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'Le modele'
        form = ModeleForm(instance=Modele.objects.last())
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            term = request.GET.get('term')
            marques = Marque.objects.all().filter(nom_marque__icontains=term)
            return JsonResponse(list(marques.values()), safe=False)
        
        if request.method == "POST":
            form = ModeleForm(request.POST, instance=Modele.objects.last())
            if form.is_valid():
                
                marque_id = form.cleaned_data['marque']
                marque = Marque.objects.get(id=marque_id.id)
                nom_modele = form.cleaned_data['nom_modele']
                annee = form.cleaned_data['annee']
                existing_modele = Modele.objects.filter(nom_modele=nom_modele, marque=marque, annee=annee).first()
                if existing_modele:
                    messages.error(request, 'Un modèle avec ce nom et cette marque existe déjà.')
                else:  
                    form.save()
                    modele_instance = form.save()
                    return redirect(reverse('gestionnaire:details',args=[modele_instance.id, sujet]))  
        else:
            form = ModeleForm(instance=Modele.objects.last())
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet, 
                                                              'personne':personne,
                                                              'grade_id':grade_id, 
                                                              'grade':grade})
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

@login_required
def create_fournisseur(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'Le fournisseur'
        
        if request.method == "POST":
            form = FournisseurForm(request.POST)
            if form.is_valid():
                nom_fournisseur = form.cleaned_data['nom_fournisseur']
                adresse = form.cleaned_data['adresse']
                description_fournisseur = form.cleaned_data['description_fournisseur']
                existing_fournisseur = Fournisseur.objects.filter(nom_fournisseur=nom_fournisseur).first()
                if existing_fournisseur:
                    messages.error(request, 'Un fournisseur avec ce nom existe déjà.')
                else:
                    fournisseur=Fournisseur(
                        nom_fournisseur=nom_fournisseur,
                        adresse=adresse,
                        description_fournisseur=description_fournisseur,
                    )
                    fournisseur.save()
                    return redirect(reverse('gestionnaire:details',args=[fournisseur.id, sujet]))  
        else:
            form = FournisseurForm()
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet, 
                                                              'personne':personne,
                                                              'grade_id':grade_id, 
                                                              'grade':grade})
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

@login_required
def create_engin(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'l\'engin'
        
        form = EnginForm(instance=Engin.objects.last())
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            term=request.GET.get('term')
            field_name=request.GET.get('field_name')
            
            if field_name == 'modele_engin':
                modele=Modele.objects.all().filter(nom_modele__icontains=term)
                return JsonResponse(list(modele.values()), safe=False)
            elif field_name == 'fournisseur_engin':
                fournisseurs=Fournisseur.objects.all().filter(nom_fournisseur__icontains=term)
                return JsonResponse(list(fournisseurs.values()), safe=False)
            elif field_name == 'info_engin':
                infos=Fournisseur.objects.all().filter(info__icontains=term)
                return JsonResponse(list(infos.values()), safe=False)
            
        if request.method == "POST":
            form = EnginForm(request.POST,instance=Engin.objects.last())
            if form.is_valid():
                immatriculation = form.cleaned_data['immatriculation']
                existing_engin = Engin.objects.filter(immatriculation=immatriculation).first()
                if existing_engin:
                    messages.error(request, 'Un engin avec ce numéro d\'immatriculation existe déjà.')
                else:
                    couleur = form.cleaned_data['couleur']
                    capa_reserv = form.cleaned_data['capa_reserv']
                    modele_id = form.cleaned_data['modele_engin']
                    modele = Modele.objects.get(id=modele_id)
                    
                    type_engin_id = form.cleaned_data['type_engin']
                    type_engin = TypeEngin.objects.get(id=type_engin_id)
                    
                    info_engin_id = form.cleaned_data['info_engin']  
                    info_engin = InfoEngin.objects.get(id=info_engin_id)
                    
                    etat_engin_id = form.cleaned_data['etat_engin']
                    etat_engin = EtatEngin.objects.get(id=etat_engin_id)
                    
                    fournisseur_engin_id = form.cleaned_data['fournisseur_engin']
                    fournisseur_engin = Fournisseur.objects.get(id=fournisseur_engin_id)
                    
                    est_obsolete = form.cleaned_data['est_obsolete']
                    vik = form.cleaned_data['vik']
                    engin = Engin(
                        immatriculation=immatriculation,
                        couleur=couleur,
                        modele_engin=modele,
                        type_engin=type_engin,
                        info_engin=info_engin,  
                        etat_engin=etat_engin,  
                        fournisseur_engin=fournisseur_engin,  
                        est_obsolete=est_obsolete,
                        vik=vik,
                        capa_reserv=capa_reserv,
                    )
                    engin.save()
                    print('id = ',engin.id)
                    return redirect(reverse('gestionnaire:details', args=[engin.id, sujet]))  
        else:
            form = EnginForm(instance=Engin.objects.last())
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet,
                                                              'personne':personne, 
                                                              'grade_id':grade_id, 
                                                              'grade':grade})
    else:
    # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})


@login_required
def create_type_engin(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'Le type d\'engin'
        
        if request.method == "POST":
            form = TypeEnginForm(request.POST)
            if form.is_valid():
                designation = form.cleaned_data['designation']
                existing_type_engin = TypeEngin.objects.filter(designation=designation).first()
                if existing_type_engin:
                    messages.error(request, 'Un type d''engin avec ce libellé de désignation existe déjà.')
                else:
                    description=form.cleaned_data['description']
                    nombre_roue=form.cleaned_data['nombre_roue']
                    
                    type_engin=TypeEngin(
                        designation=designation,
                        description=description,
                        nombre_roue=nombre_roue,
                    )
                    type_engin.save()
                    return redirect(reverse('gestionnaire:details',args=[type_engin.id, sujet]))  
        else:
            form = TypeEnginForm()
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet,
                                                              'personne':personne, 
                                                              'grade_id':grade_id, 
                                                              'grade':grade})


@login_required
def create_etat_engin(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'L\'état de l\'engin'
        
        if request.method == "POST":
            form = EtatEnginForm(request.POST)
            if form.is_valid():
                libelle_etat = form.cleaned_data['libelle_etat']
                existing_etat_engin = EtatEngin.objects.filter(libelle_etat=libelle_etat).first()
                if existing_etat_engin:
                    messages.error(request, 'Un état d\'engin avec ce libellé existe déjà.')
                else:
                    etat_engin=EtatEngin(
                        libelle_etat=libelle_etat,
                    )
                    etat_engin.save()
                    return redirect(reverse('gestionnaire:details',args=[etat_engin.id, sujet]))  
        else:
            form = EtatEnginForm()
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet, 
                                                              'grade_id':grade_id, 
                                                              'grade':grade})


@login_required
def create_info_engin(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'info_engin'
        
        if request.method == "POST":
            form = InfoEnginForm(request.POST)
            if form.is_valid():
                info = form.cleaned_data['info']
                existing_info_engin = InfoEngin.objects.filter(info=info).first()
                if existing_info_engin:
                    messages.error(request, 'Des informations d\'engin avec ce libellé existent déjà.')
                else:
                    consommation=form.cleaned_data['consommation']
                    vidange=form.cleaned_data['vidange']
                    revision=form.cleaned_data['revision']
                    
                    info_engin=InfoEngin(
                        info=info,
                        consommation=consommation,
                        vidange=vidange,
                        revision=revision,
                    )
                    info_engin.save()
                    return redirect(reverse('gestionnaire:details',args=[info_engin.id, sujet]))  
        else:
            form = InfoEnginForm()
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet, 
                                                              'grade_id':grade_id, 
                                                              'grade':grade})
    

@login_required
def create_ravitaillement_carburant(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='ravitaillement_carburant'
        solde2=0
        
        form = RavitaillementCarburantForm(instance=RavitaillementCarburant.objects.last())
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            term=request.GET.get('term')
            field_name=request.GET.get('field_name')
            
            if field_name == 'engin_rav':
                engins_rav=Engin.objects.all().filter(immatriculation__icontains=term)
                return JsonResponse(list(engins_rav.values()), safe=False)
            elif field_name == 'fournisseur_carburant':
                fournisseurscarb=Fournisseur.objects.all().filter(nom_fournisseur__icontains=term)
                return JsonResponse(list(fournisseurscarb.values()), safe=False)
            
        if request.method == "POST":
            form = RavitaillementCarburantForm(request.POST,instance=RavitaillementCarburant.objects.last())
            if form.is_valid():
                date_actuelle = datetime.datetime.now()
                cout_rav=form.cleaned_data['cout_rav']
                quantite_rav=cout_rav/700
                engin_rav_id = form.cleaned_data['engin_rav']
                engin_rav = Engin.objects.get(id=engin_rav_id.id)
                fournisseur_carburant_id = form.cleaned_data['fournisseur_carburant']
                fournisseur_carburant = Fournisseur.objects.get(id=fournisseur_carburant_id.id)
                date_max_precedente = ReleveDistance.objects.filter(engin_releve=engin_rav, date_releve__lt=date_actuelle).aggregate(Max('date_releve'))['date_releve__max']
                enregistrement_precedent = ReleveDistance.objects.filter(engin_releve=engin_rav, date_releve=date_max_precedente).first()
                date_rav_precedente = RavitaillementCarburant.objects.filter(engin_rav=engin_rav, date_rav__lt=date_actuelle).aggregate(Max('date_rav'))['date_rav__max']
                carb_precedent = RavitaillementCarburant.objects.filter(engin_rav=engin_rav, date_rav=date_rav_precedente).first()
                # carb_restant = float(enregistrement_precedent.last().carb_dispo) if enregistrement_precedent.exists() else 0
                if enregistrement_precedent or carb_precedent:
                    carb_restant = enregistrement_precedent.carb_restant
                    if carb_restant is not None:
                        carb_restant = float(carb_restant)
                        
                    else:
                        carb_restant = carb_precedent
                else:
                    carb_restant = 0
                    
                carb_dispo = carb_restant + quantite_rav
                plein = form.cleaned_data['plein']
                if plein : 
                    Km_plein = form.cleaned_data['Km_plein']
                    
                date_actuelle = datetime.datetime.now()
                date_max_precedente = RavitaillementCarburant.objects.filter(engin_rav=engin_rav, date_rav__lt=date_actuelle).aggregate(Max('date_rav'))['date_rav__max']
                enregistrement_precedent = RavitaillementCarburant.objects.filter(engin_rav=engin_rav, date_rav=date_max_precedente).first()
                
                if enregistrement_precedent and plein:
                    km1 = enregistrement_precedent.Km_plein
                    donnee_conso = engin_rav.info_engin.consommation
                    conso = (Km_plein - km1)*donnee_conso
                    
                    ravitaillement_carburant=RavitaillementCarburant(
                    cout_rav=cout_rav,
                    quantite_rav=quantite_rav,
                    engin_rav=engin_rav_id,
                    fournisseur_carburant=fournisseur_carburant_id,
                    carb_dispo=carb_dispo,
                    plein=plein,
                    Km_plein=Km_plein,
                    conso=conso,
                )
                else:
                    ravitaillement_carburant=RavitaillementCarburant(
                    cout_rav=cout_rav,
                    quantite_rav=quantite_rav,
                    engin_rav=engin_rav_id,
                    fournisseur_carburant=fournisseur_carburant_id,
                    carb_dispo=carb_dispo,
                    plein=plein,
                )
                    
                ravitaillement_carburant.save()
                
                type_engin_tcard = engin_rav.type_engin
                solde1 = T_Card.objects.filter(type_engin_tcard=type_engin_tcard).values_list('solde',flat=True).last()
                solde2 = solde1 - cout_rav
                
                t_card = T_Card(
                    type_engin_tcard = type_engin_tcard,
                    montant = cout_rav,
                    solde = solde2,
                )
                t_card.save()
                
                return redirect(reverse('gestionnaire:details',args=[ravitaillement_carburant.id, sujet]))  
        else:
            form = RavitaillementCarburantForm(instance=RavitaillementCarburant.objects.last())
        return render(request,'gestionnaire/creation.html',{'form':form,
                                                            'sujet':sujet,
                                                            'personne':personne,                                                            'grade_id':grade_id, 
                                                            'grade':grade, 
                                                            'solde2':solde2})
    

@login_required
def create_type_maintenance(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'type_maintenance'
        
        if request.method == "POST":
            form = TypeMaintenanceForm(request.POST)
            if form.is_valid():
                libelle_maint = form.cleaned_data['libelle_maint']
                existing_type_maintenance = TypeMaintenance.objects.filter(libelle_maint=libelle_maint).first()
                if existing_type_maintenance:
                    messages.error(request, 'Un type de maintenance avec ce libellé existe déjà.')
                else:
                    type_maintenance=TypeMaintenance(
                        libelle_maint=libelle_maint,
                    )
                    type_maintenance.save()
                    return redirect(reverse('gestionnaire:details',args=[type_maintenance.id , sujet]))  
        else:
            form = TypeMaintenanceForm()
            
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet, 
                                                              'personne':personne,
                                                              'grade_id':grade_id, 
                                                              'grade':grade})


@login_required
def create_maintenance_engin(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        
        sujet = 'maintenance_engin'
        form = MaintenanceEnginForm(instance=MaintenanceEngin.objects.last())

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            term = request.GET.get('term')
            field_name = request.GET.get('field_name')

            if field_name == 'engin_maint':
                engins = Engin.objects.all().filter(immatriculation__icontains=term)
                return JsonResponse(list(engins.values()), safe=False)
            elif field_name == 'fournisseur_maint':
                fournisseurs = Fournisseur.objects.all().filter(nom_fournisseur__icontains=term)
                return JsonResponse(list(fournisseurs.values()), safe=False)
            
        if request.method == "POST":
            form = MaintenanceEnginForm(request.POST, instance=MaintenanceEngin.objects.last())
            
            if form.is_valid():
                date_maint = datetime.datetime.now()
                engin_id = form.cleaned_data['engin_maint'].id
                engin_maint = Engin.objects.get(id=engin_id)
                motif_maint = form.cleaned_data['motif_maint']
                type_id = form.cleaned_data['type_maint'].id
                type_maint = TypeMaintenance.objects.get(id=type_id)
                fournisseur_id = form.cleaned_data['fournisseur_maint'].id
                fournisseur_maint = Fournisseur.objects.get(id=fournisseur_id)
                cout_maint = form.cleaned_data['cout_maint']
                
                maintenance = MaintenanceEngin(
                    motif_maint=motif_maint,
                    date_maint=date_maint,
                    engin_maint=engin_maint,
                    type_maint=type_maint,
                    fournisseur_maint=fournisseur_maint,
                    cout_maint=cout_maint
                )
                maintenance.save()
            
                update_notifications(engin_maint.id)
                return redirect(reverse('gestionnaire:details', args=[maintenance.id, sujet]))
        else:
            form = MaintenanceEnginForm(instance=MaintenanceEngin.objects.last())
        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet,
                                                              'personne':personne, 
                                                              'grade_id': grade_id, 
                                                              'grade': grade})



@login_required
def create_attribution(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'attribution'
        form = AttributionForm(instance=Attribution.objects.last())

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            term = request.GET.get('term')
            field_name = request.GET.get('field_name')

            if field_name == 'engin':
                engins = Engin.objects.all().filter(immatriculation__icontains=term)
                return JsonResponse(list(engins.values()), safe=False)
            elif field_name == 'conducteur':
                conducteurs = Personne.objects.all().filter(nom__icontains=term)
                return JsonResponse(list(conducteurs.values()), safe=False)

        if request.method == "POST":
            form = AttributionForm(request.POST, instance=Attribution.objects.last())
            if form.is_valid():
                form.save()
                attribution_instance = form.save()
                return redirect(reverse('gestionnaire:details', args=[attribution_instance.id, sujet]))
        else:
            form = AttributionForm(instance=Attribution.objects.last())

        return render(request, 'gestionnaire/creation.html', {'form': form, 
                                                              'sujet': sujet,
                                                              'personne':personne, 
                                                              'grade_id': grade_id, 
                                                              'grade': grade})

@login_required
def create_releve_distance(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='relevé de distance'
        form = ReleveDistanceForm(instance=ReleveDistance.objects.last())
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            term = request.GET.get('term')
            engins = Engin.objects.all().filter(immatriculation__icontains=term)
            return JsonResponse(list(engins.values()), safe=False)
            
        if request.method == "POST":
            form = ReleveDistanceForm(request.POST,instance=ReleveDistance.objects.last())
            if form.is_valid():
                nbKmFin=form.cleaned_data['nbKmFin']
                engin_releve_id = form.cleaned_data['engin_releve']
                engin_releve = Engin.objects.get(id=engin_releve_id.id)
                print('Engin : ', engin_releve_id)
                releves = ReleveDistance.objects.filter(engin_releve=engin_releve_id)
                if releves.exists():
                    nbKmDebut = float(releves.last().nbKmFin) if releves.exists() else 0
                else :
                    nbKmDebut = engin_releve.vik
                distance = nbKmFin - nbKmDebut
                mode_4x4 = form.cleaned_data['mode_4x4']
                date_actuelle = datetime.datetime.now()
                # la date maximale précédant la date actuelle pour le même engin
                date_max_precedente = ReleveDistance.objects.filter(engin_releve=engin_releve, date_releve__lt=date_actuelle).aggregate(Max('date_releve'))['date_releve__max']

                # enregistrement précédent pour le même engin et la date maximale précédente
                enregistrement_precedent = ReleveDistance.objects.filter(engin_releve=engin_releve, date_releve=date_max_precedente).last()
                if enregistrement_precedent:
                    carb_depart = enregistrement_precedent.carb_restant
                else:
                    # Il n'y a pas d'enregistrement précédent
                    carb_depart = None
                date_max_prec_conso = RavitaillementCarburant.objects.filter(engin_rav=engin_releve, date_rav__lt=date_actuelle).aggregate(Max('date_rav'))['date_rav__max']
                enregistrement_prec_conso = RavitaillementCarburant.objects.filter(engin_rav=engin_releve, date_rav=date_max_prec_conso).last()
                if enregistrement_prec_conso:
                    qte = enregistrement_prec_conso.quantite_rav
                    date_r = enregistrement_prec_conso.date_rav
                else:
                    # Il n'y a pas d'enregistrement précédent
                    qte = None
                    date_r = None
                carb_consomme = distance*engin_releve.info_engin.consommation/100
                if carb_depart is not None and carb_consomme is not None:
                    carb_restant = carb_depart - carb_consomme
                else:
                    if carb_depart is None:
                        carb_restant = 0
                    else : 
                        carb_restant = carb_depart
                    
                ravitaillement = form.cleaned_data['ravitaillement']
                qte_rav = qte
                date2_rav = date_r
                
                releve_distance=ReleveDistance(
                    nbKmDebut=nbKmDebut,
                    nbKmFin=nbKmFin,
                    engin_releve=engin_releve,
                    distance=distance,
                    mode_4x4 = mode_4x4,
                    carb_depart =carb_depart,
                    carb_consomme = carb_consomme,
                    carb_restant = carb_restant,
                    ravitaillement = ravitaillement,
                    qte_rav = qte_rav,
                    date2_rav = date2_rav,
                )
                releve_distance.save()
                engin_releve.nja += 1 
                engin_releve.save()
                return redirect(reverse('gestionnaire:details',args=[releve_distance.id, sujet]))  
        else:
            form = ReleveDistanceForm(instance=ReleveDistance.objects.last())
        return render(request,'gestionnaire/creation.html',{'form':form,
                                                            'sujet':sujet,
                                                            'personne':personne,
                                                            'grade_id':grade_id,  
                                                            'grade':grade})
    

@login_required
def create_t_card(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='t_card'
        if request.method == 'POST':
            form = T_CardForm(request.POST)
            if form.is_valid():
                type_engin_tcard_id = form.cleaned_data['type_engin_tcard']
                type_engin_tcard = TypeEngin.objects.get(id=type_engin_tcard_id)
                montant = form.cleaned_data['montant']
                approvisionnement = True
                
                t_card = T_Card(
                    type_engin_tcard=type_engin_tcard,
                    solde=montant,
                    montant=montant,
                    approvisionnement=approvisionnement,
                )
                t_card.save()
                print('les informations : ', t_card.type_engin_tcard,' | ', t_card.solde )
                return redirect(reverse('gestionnaire:details',args=[t_card.id, sujet]))
        else:
            form = T_CardForm()
        return render(request,'gestionnaire/creation.html',{'form':form,
                                                            'sujet':sujet,
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

"""
LES UPDATES

@login_required"""  
def update_personne(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='personne'
        personne_update = get_object_or_404(Personne, pk=pk)
        if request.method == 'POST':
            form = PersonneForm(request.POST)
            if form.is_valid():
                personne_update.nom = form.cleaned_data['nom']
                personne_update.prenom = form.cleaned_data['prenom']
                personne_update.contact = form.cleaned_data['contact']
                personne_update.grade = form.cleaned_data['grade']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = PersonneForm(initial={
                'nom' : personne_update.nom,
                'prenom' : personne_update.prenom,
                'contact' : personne_update.contact,
                'grade' : personne_update.grade,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet, 
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_type_engin(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='type_engin'
        type_engin = get_object_or_404(TypeEngin, pk=pk)
        if request.method == 'POST':
            form = TypeEnginForm(request.POST, instance=type_engin)
            if form.is_valid():
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = TypeEnginForm(instance=type_engin)
        return render(request, 'gestionnaire/update.html', {'form': form,
                                                            'personne':personne, 
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_modele(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='modele'
        modele = get_object_or_404(Modele, pk=pk)
        if request.method == 'POST':
            form = ModeleForm(request.POST, instance=modele)
            if form.is_valid():
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = ModeleForm(instance=modele)
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_fournisseur(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='fournisseur'
        fournisseur = get_object_or_404(Fournisseur, pk=pk)
        if request.method == 'POST':
            form = FournisseurForm(request.POST, instance=fournisseur)
            if form.is_valid():
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = FournisseurForm(instance=fournisseur)
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_info_engin(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='info_engin'
        information = get_object_or_404(InfoEngin, pk=pk)
        if request.method == 'POST':
            form = InfoEnginForm(request.POST)
            if form.is_valid():
                information.info = form.cleaned_data['info']
                information.consommation = form.cleaned_data['consommation']
                information.vidange = form.cleaned_data['vidange']
                information.revision = form.cleaned_data['revision']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = InfoEnginForm(initial={
                'info' : information.info,
                'consommation' : information.consommation,
                'vidange' : information.vidange,
                'revision' : information.revision,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet, 
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_ravitaillement_carburant(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='ravitaillement_carburant'
        ravitaillement_carburant = get_object_or_404(RavitaillementCarburant, pk=pk)
        if request.method == 'POST':
            form = RavitaillementCarburantForm(request.POST)
            if form.is_valid():
                ravitaillement_carburant.cout_rav = form.cleaned_data['cout_rav']
                ravitaillement_carburant.engin_rav = form.cleaned_data['engin_rav']
                ravitaillement_carburant.fournisseur_carburant = form.cleaned_data['fournisseur_carburant']
                ravitaillement_carburant.plein = form.cleaned_data['plein']
                ravitaillement_carburant.Km_plein = form.cleaned_data['Km_plein']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = RavitaillementCarburantForm(initial={
                'cout_rav' : ravitaillement_carburant.cout_rav,
                'engin_rav' : ravitaillement_carburant.engin_rav,
                'fournisseur_carburant' : ravitaillement_carburant.fournisseur_carburant,
                'plein' : ravitaillement_carburant.plein,
                'Km_plein' : ravitaillement_carburant.Km_plein,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'personne':personne, 
                                                            'sujet':sujet, 
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_engin(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 'engin'
        engin = get_object_or_404(Engin, pk=pk)
        
        if request.method == 'POST':
            form = EnginForm(request.POST)
            if form.is_valid():
                engin.immatriculation = form.cleaned_data['immatriculation']
                engin.couleur = form.cleaned_data['couleur']
                engin.modele_engin = form.cleaned_data['modele_engin']
                engin.type_engin = form.cleaned_data['type_engin']
                engin.info_engin = form.cleaned_data['info_engin']
                engin.etat_engin = form.cleaned_data['etat_engin']
                engin.est_obsolete = form.cleaned_data['est_obsolete']
                engin.fournisseur_engin = form.cleaned_data['fournisseur_engin']
                engin.vik = form.cleaned_data['vik']
                engin.capa_reserv = form.cleaned_data['capa_reserv']
                
                engin.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))
        else:
            form = EnginForm(initial={
                'immatriculation': engin.immatriculation,
                'couleur': engin.couleur,
                'modele_engin': engin.modele_engin,
                'type_engin': engin.type_engin,
                'info_engin': engin.info_engin,
                'etat_engin': engin.etat_engin,
                'est_obsolete': engin.est_obsolete,
                'fournisseur_engin': engin.fournisseur_engin,
                'vik': engin.vik,
                'capa_reserv': engin.capa_reserv,
            })
        
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'personne':personne, 
                                                            'grade_id': grade_id,
                                                            'grade': grade, 
                                                            'sujet':sujet})


@login_required
def update_marque(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='marque'
        marque = get_object_or_404(Marque, pk=pk)
        if request.method == 'POST':
            form = MarqueForm(request.POST, instance=marque)
            if form.is_valid():
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = MarqueForm(instance=marque)
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_etat_engin(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='etat_engin'
        etat_engin = get_object_or_404(EtatEngin, pk=pk)
        if request.method == 'POST':
            form = EtatEnginForm(request.POST, instance=etat_engin)
            if form.is_valid():
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = EtatEnginForm(instance=etat_engin)
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet,
                                                            'personne':personne, 
                                                            'grade_id':grade_id, 
                                                            'grade':grade})


@login_required
def update_maintenance_engin(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='maintenance_engin'
        maintenance_engin = get_object_or_404(MaintenanceEngin, pk=pk)
        if request.method == 'POST':
            form = MaintenanceEnginForm(request.POST)
            if form.is_valid():
                maintenance_engin.type_maint = form.cleaned_data['type_maint']
                maintenance_engin.motif_maint = form.cleaned_data['motif_maint']
                maintenance_engin.engin_maint = form.cleaned_data['engin_maint']
                maintenance_engin.cout_maint = form.cleaned_data['cout_maint']
                maintenance_engin.fournisseur_maint = form.cleaned_data['fournisseur_maint']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = MaintenanceEnginForm(initial={
                'type_maint' : maintenance_engin.type_maint,
                'motif_maint' : maintenance_engin.motif_maint,
                'engin_maint' : maintenance_engin.engin_maint,
                'cout_maint' : maintenance_engin.cout_maint,
                'fournisseur_maint': maintenance_engin.fournisseur_maint,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet,
                                                            'personne':personne, 
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_type_maintenance(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='type_maintenance'
        type_maintenance = get_object_or_404(TypeMaintenance, pk=pk)
        if request.method == 'POST':
            form = TypeMaintenanceForm(request.POST)
            if form.is_valid():
                type_maintenance.libelle_maint = form.cleaned_data['libelle_maint']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = TypeMaintenanceForm(initial={
                'libelle_maint' : type_maintenance.libelle_maint,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet, 
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_attribution(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='attribution'
        attribution = get_object_or_404(Attribution, pk=pk)
        if request.method == 'POST':
            form = AttributionForm(request.POST)
            if form.is_valid():
                attribution.conducteur = form.cleaned_data['conducteur']
                attribution.engin = form.cleaned_data['engin']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = AttributionForm(initial={
                'conducteur' : attribution.conducteur,
                'engin' : attribution.engin,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet, 
                                                            'personne':personne,
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_releve_distance(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='releve_distance'
        releve_distance = get_object_or_404(ReleveDistance, pk=pk)
        if request.method == 'POST':
            form = ReleveDistanceForm(request.POST)
            if form.is_valid():
                releve_distance.engin_releve = form.cleaned_data['engin_releve']
                releve_distance.nbKmFin = form.cleaned_data['nbKmFin']
                releve_distance.mode_4x4 = form.cleaned_data['mode_4x4']
                releve_distance.ravitaillement = form.cleaned_data['ravitaillement']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[sujet]))  
        else:
            form = ReleveDistanceForm(initial={
                'engin_releve' : releve_distance.engin_releve,
                'nbKmFin' : releve_distance.nbKmFin,
                'mode_4x4' : releve_distance.mode_4x4,
                'ravitaillement' : releve_distance.ravitaillement,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet,
                                                            'personne':personne, 
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def option_t_card(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 't_card'
        t_card = T_Card.objects.all()
        moto = T_Card.objects.filter(type_engin_tcard=1)
        tricycle = T_Card.objects.filter(type_engin_tcard=2)
        voiture = T_Card.objects.filter(type_engin_tcard=3)
        type_engin = TypeEngin.objects.all()
        type_engin_id = None  
        solde_moto = float(moto.last().solde) if moto.exists() else 0
        solde_tricycle = float(tricycle.last().solde) if tricycle.exists() else 0
        solde_voiture = float(voiture.last().solde) if voiture.exists() else 0
        if request.method == 'POST':
            type_engin_id = request.POST.get('type_engin_tcard')
            print('type engin card', type_engin_id)
            
            return redirect(reverse('gestionnaire:update_t_card', args=[type_engin_id, 'approvisionnement']))
        
        return render(request, 'gestionnaire/t_card_option.html', {
            'sujet': sujet,
            'personne':personne,
            'grade_id': grade_id,
            'grade': grade,
            't_card': t_card,
            'type_engin': type_engin,
            'type_engin_tcard_id': type_engin_id,
            'moto': moto,
            'tricycle': tricycle,
            'voiture': voiture,
            'solde_moto': solde_moto,
            'solde_tricycle': solde_tricycle,
            'solde_voiture': solde_voiture,
        })

@login_required
def edit_t_card(request, pk):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='t_card'
        t_card = get_object_or_404(T_Card, pk=pk)
        if request.method == 'POST':
            form = T_CardForm(request.POST)
            if form.is_valid():
                t_card.montant = form.cleaned_data['montant']
                t_card.type_engin_tcard = form.cleaned_data['type_engin_tcard']
                form.save()
                return redirect(reverse('gestionnaire:details', args=[pk, sujet]))  
        else:
            form = T_CardForm(initial={
                'montant' : t_card.montant,
                'type_engin_tcard' : t_card.type_engin_tcard,
            })
        return render(request, 'gestionnaire/update.html', {'form': form, 
                                                            'sujet':sujet,
                                                            'personne':personne, 
                                                            'grade_id':grade_id, 
                                                            'grade':grade})

@login_required
def update_t_card(request, pk, action):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet = 't_card'
        t_card = T_Card.objects.filter(type_engin_tcard=pk)  
        last_solde = float(t_card.last().solde) if t_card.exists() else 0
        
        type_carte =  TypeEngin.objects.filter(id=pk)
        type_carte=type_carte[0].designation
        
        if request.method == 'POST':
            form = T_CardForm(request.POST)
            if form.is_valid():
                montant = float(form.cleaned_data['montant'])
                type_engin_tcard=pk
                solde2 = 0
                if action == 'approvisionnement':
                    solde2 = last_solde + montant
                    approvisionnement = True
                else:
                    solde2 = last_solde - montant
                    approvisionnement = False
                t_card = T_Card(
                    montant=montant,
                    type_engin_tcard=type_engin_tcard,
                    solde=solde2,
                    approvisionnement=approvisionnement,
                )
                t_card.save()
                return redirect('gestionnaire:details', pk=pk, sujet=sujet)  # Utilisez simplement les noms d'arguments

        else:
            form = T_CardForm()

        return render(request, 'gestionnaire/update.html', {
            'form': form,
            'sujet': sujet,
            'personne':personne,
            'action': action,
            'grade_id': grade_id,
            'grade': grade,
            'type_carte':type_carte,
    })


"""
LES DELETE
"""

@login_required
def delete_modele(request, modele_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='modele'
        modele = get_object_or_404(Modele, pk=modele_id)
        if request.method == 'POST':
            modele.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))  
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'modele'})

@login_required
def delete_info_engin(request, info_engin_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='info_engin'
        info_engin = get_object_or_404(InfoEngin, pk=info_engin_id)
        
        if request.method == 'POST':
            info_engin.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'info_engin'})

@login_required
def delete_ravitaillement_carburant(request, ravitaillement_carburant_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='ravitaillement_carburant'
        ravitaillement_carburant = get_object_or_404(RavitaillementCarburant, pk=ravitaillement_carburant_id)
        
        if request.method == 'POST':
            ravitaillement_carburant.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'ravitaillement_carburant'})

@login_required
def delete_personne(request, personne_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='personne'
        personne = get_object_or_404(Personne, pk=personne_id)
        
        if request.method == 'POST':
            personne.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'personne'})

@login_required
def delete_marque(request, marque_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='marque'
        marque = get_object_or_404(Marque, pk=marque_id)
        
        if request.method == 'POST':
            marque.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'marque'})

@login_required
def delete_fournisseur(request, fournisseur_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='fournisseur'
        fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
        
        if request.method == 'POST':
            fournisseur.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'fournisseur'})

@login_required
def delete_engin(request, engin_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='engin'
        engin = get_object_or_404(Engin, pk=engin_id)
        
        if request.method == 'POST':
            engin.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'engin'})

@login_required
def delete_type_engin(request, type_engin_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='type_engin'
        type_engin = get_object_or_404(TypeEngin, pk=type_engin_id)
        
        if request.method == 'POST':
            type_engin.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'type_engin'})

@login_required
def delete_etat_engin(request, etat_engin_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='etat_engin'
        etat_engin = get_object_or_404(EtatEngin, pk=etat_engin_id)
        
        if request.method == 'POST':
            etat_engin.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'grade_id':grade_id, 'personne':personne, 'grade':grade, 'sujet': 'etat_engin'})

@login_required
def delete_type_maintenance(request, type_maintenance_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='type_maintenance'
        type_maintenance = get_object_or_404(TypeMaintenance, pk=type_maintenance_id)
        
        if request.method == 'POST':
            type_maintenance.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'personne':personne, 'grade_id':grade_id, 'grade':grade, 'sujet': 'type_maintenance'})

@login_required
def delete_maintenance_engin(request, maintenance_engin_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='maintenance_engin'
        maintenance_engin = get_object_or_404(MaintenanceEngin, pk=maintenance_engin_id)
        
        if request.method == 'POST':
            maintenance_engin.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'personne':personne, 'grade_id':grade_id, 'grade':grade, 'sujet': 'maintenance_engin'})

@login_required
def delete_attribution(request, attribution_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='attribution'
        attribution = get_object_or_404(Attribution, pk=attribution_id)
        
        if request.method == 'POST':
            attribution.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'personne':personne, 'grade_id':grade_id, 'grade':grade, 'sujet': 'attribution'})

@login_required
def delete_releve_distance(request, releve_distance_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        sujet='releve_distance'
        releve_distance = get_object_or_404(ReleveDistance, pk=releve_distance_id)
        
        if request.method == 'POST':
            releve_distance.delete()
            return redirect(reverse('gestionnaire:lists', args=[sujet]))
        
        return render(request, 'gestionnaire/delete.html', {'personne':personne, 'grade_id':grade_id, 'grade':grade, 'sujet': 'releve_distance'})
