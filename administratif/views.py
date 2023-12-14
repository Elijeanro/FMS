from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestionnaire.views import update_notifications
from django.core.paginator import Paginator
from gestionnaire.models import (Personne,Engin,Grade,Marque,Modele,TypeEngin,Fournisseur
                                 ,MaintenanceEngin,RavitaillementCarburant,ReleveDistance,T_Card)
from django.contrib.auth.forms import AuthenticationForm

ERROR_MESSAGE = 'Identifiant ou mot de passe incorrect!'
INVALID_FORM_MESSAGE = 'Formulaire invalide. Veuillez vérifier les champs.'

def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                try:
                    personne = get_object_or_404(Personne, utilisateur=user)
                    request.session['personne_id'] = personne.id
                    print(personne)
                    return redirect(reverse('administratif:espace_utilisateur'))
                except Personne.DoesNotExist:
                    messages.error(request, ERROR_MESSAGE)
            else:
                messages.error(request, ERROR_MESSAGE)
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
    else:
        form = AuthenticationForm()

    engins_avec_notifications = Engin.objects.filter(has_notification=True)
    context = {'engins_avec_notifications': engins_avec_notifications, 'form': form}
    return render(request, 'login.html', context)


def signout(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté(e) avec succès!')
    return redirect(reverse('administratif:login'))

"""
    Erreur 404
"""
def erreur_404(request):
    message = request.GET.get('message', '')
    return render(request, 'erreur404.html', {'message':message})

"""
    Espace de travail
"""
def espaceDeTravail(request):
    context = {}
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        context['personne']=personne
        grade_id=personne.grade.id
        context['grade_id']=grade_id
        print(personne)
        print(grade_id)
        
        engin = Engin.objects.all()
        page = request.GET.get('page')
        paginator = Paginator(engin, 3)
        engin = paginator.get_page(page)
        context['engin'] = engin
        
        if request.method == "POST":
            num_objet = int(request.POST.get('objet', ''))
            chaine = request.POST.get('chaine', '')

            if num_objet == 1:
                resultat = Engin.objects.filter(immatriculation__icontains=chaine)
            elif num_objet == 2:
                resultat = Engin.objects.filter(couleur__icontains=chaine)
            elif num_objet == 3:
                valeur = Marque.objects.filter(nom_marque__icontains=chaine).values_list('id', flat=True)
                valeur2 = Modele.objects.filter(marque__in=valeur).values_list('id', flat=True)
                resultat = Engin.objects.filter(modele_engin__in=valeur2)
            elif num_objet == 4:
                valeur = Modele.objects.filter(nom_modele__icontains=chaine).values_list('id', flat=True)
                resultat = Engin.objects.filter(modele_engin__in=valeur)
            elif num_objet == 5:
                valeur = TypeEngin.objects.filter(designation__icontains=chaine).values_list('id', flat=True)
                resultat = Engin.objects.filter(type_engin__in=valeur)
            elif num_objet == 6:
                valeur = Fournisseur.objects.filter(nom_fournisseur__icontains=chaine).values_list('id', flat=True)
                resultat = Engin.objects.filter(fournisseur_engin__in=valeur)
            else:
                resultat = engin

            context['engin'] = resultat

        engins_avec_notifications = Engin.objects.filter(has_notification=True)
        nb_engin_notif = engins_avec_notifications.count()
        context['nb_engin_notif'] = nb_engin_notif
        context['engins_avec_notifications'] = engins_avec_notifications

        return render(request, 'espace_de_travail.html', context)
    else:
        # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})
    
"""
    Les analyses
"""
def analyse_glob(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)

        maintenances = MaintenanceEngin.objects.all().order_by('-date_maint')
        vidanges = MaintenanceEngin.objects.filter(type_maint=4).order_by('-date_maint')
        releves = ReleveDistance.objects.all().order_by('-date_releve')
        ravitaillements = RavitaillementCarburant.objects.all().order_by('-date_rav')

        # Initialisation de la variable pour stocker les données d'écart de consommation
        ecart_conso_data = []  
        prev_ravitaillement = None  

        for ravitaillement in ravitaillements:
            if prev_ravitaillement and ravitaillement.Km_plein is not None and prev_ravitaillement.Km_plein is not None:
                ecart = float(ravitaillement.Km_plein) - float(prev_ravitaillement.Km_plein)
                ecart_conso = ((ravitaillement.quantite_rav * 100 / ecart) - ravitaillement.engin_rav.info_engin.consommation) * 100
            else:
                ecart_conso = 0  # Aucun ravitaillement précédent, ou valeurs Km_plein manquantes, définir l'écart à 0

            ecart_conso_data.append(ecart_conso)
            prev_ravitaillement = ravitaillement

    # Maintenant, ecart_conso_data contient toutes les valeurs d'écart_conso

        for i, ravitaillement in enumerate(ravitaillements):
            ravitaillement.ecart_conso = ecart_conso_data[i]

        # Tri des ravitaillements par écart de consommation
        ravitaillements = sorted(ravitaillements, key=lambda x: x.ecart_conso, reverse=True)
        nb_maintenance = maintenances.count()
        nb_vidange = vidanges.count()
        quantite_r = sum(r.quantite_rav for r in ravitaillements)
        cout_m = maintenances.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        cout_v = vidanges.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        cout_r = sum(r.cout_rav for r in ravitaillements)

        context = {
            'grade': grade,
            'grade_id': grade_id,
            'quantite_rav': quantite_r,
            'nb_maintenance': nb_maintenance,
            'nb_vidange': nb_vidange,
            'releves': releves,
            'cout_m': cout_m,
            'cout_r': cout_r,
            'cout_v': cout_v,
            'personne':personne,
        }
        engins_avec_notifications = Engin.objects.filter(has_notification=True)
        nb_engin_notif = engins_avec_notifications.count()
        context['nb_engin_notif'] = nb_engin_notif
        context['engins_avec_notifications'] = engins_avec_notifications
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(ravitaillements, 4)  # Nombre d'éléments par page
        try:
            ravitaillements = paginator.page(page)
        except PageNotAnInteger:
            ravitaillements = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            ravitaillements = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['ravitaillements'] = ravitaillements
        
        page = request.GET.get('page')
        paginator = Paginator(maintenances, 4)  # Nombre d'éléments par page
        try:
            maintenances = paginator.page(page)
        except PageNotAnInteger:
            maintenances = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            maintenances = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['maintenances'] = maintenances
        
        page = request.GET.get('page')
        paginator = Paginator(vidanges, 4)  # Nombre d'éléments par page
        try:
            vidanges = paginator.page(page)
        except PageNotAnInteger:
            vidanges = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            vidanges = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['vidanges'] = vidanges
        return render(request, 'analyse/analyses_glob.html', context)
    else:
        # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})


def analyse_partic(request, engin_id):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
        engin = get_object_or_404(Engin, pk=engin_id)
        
        maintenances = MaintenanceEngin.objects.filter(engin_maint=engin)
        ravitaillements = RavitaillementCarburant.objects.filter(engin_rav=engin)
        vidanges = MaintenanceEngin.objects.filter(type_maint=4, engin_maint=engin)
        releves = ReleveDistance.objects.filter(engin_releve=engin)
        
        # Calculez la dernière valeur de chaque QuerySet
        Km_actuel = float(releves.last().nbKmFin) if releves.exists() else 0
        Km_last_vidange = float(vidanges.last().Km_vid) if vidanges.exists() else 0
        
        distance_totale = Km_actuel - Km_last_vidange
        
        # Utilisez l'agrégation Sum pour obtenir la somme des quantités, coûts, etc.
        nb_maintenance = maintenances.count()
        nb_vidange = vidanges.count()
        quantite_r = ravitaillements.aggregate(Sum('quantite_rav'))['quantite_rav__sum'] or 0
        cout_m = maintenances.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        cout_v = vidanges.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        cout_r = ravitaillements.aggregate(Sum('cout_rav'))['cout_rav__sum'] or 0
        
        context = {
            'grade': grade,
            'grade_id': grade_id,
            'personne':personne,
            'engin': engin,
            'maintenances': maintenances,
            'ravitaillements': ravitaillements,
            'vidanges': vidanges,
            'Km_actuel': Km_actuel,
            'Km_last_vidange': Km_last_vidange,
            'distance_totale': distance_totale,
            'quantite_r': quantite_r,
            'nb_maintenance': nb_maintenance,
            'nb_vidange': nb_vidange,
            'cout_m': cout_m,
            'cout_r': cout_r,
            'cout_v': cout_v,
        }
        engins_avec_notifications = Engin.objects.filter(has_notification=True)
        nb_engin_notif = engins_avec_notifications.count()
        context['nb_engin_notif'] = nb_engin_notif
        context['engins_avec_notifications'] = engins_avec_notifications
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(ravitaillements, 4)  # Nombre d'éléments par page
        try:
            ravitaillements = paginator.page(page)
        except PageNotAnInteger:
            ravitaillements = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            ravitaillements = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['ravitaillements'] = ravitaillements
        
        page = request.GET.get('page')
        paginator = Paginator(maintenances, 4)  # Nombre d'éléments par page
        try:
            maintenances = paginator.page(page)
        except PageNotAnInteger:
            maintenances = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            maintenances = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['maintenances'] = maintenances
        
        page = request.GET.get('page')
        paginator = Paginator(vidanges, 4)  # Nombre d'éléments par page
        try:
            vidanges = paginator.page(page)
        except PageNotAnInteger:
            vidanges = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            vidanges = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['vidanges'] = vidanges

        return render(request, 'analyse/analyses_partic.html', context)
    else:
        # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

"""
    Le bilan périodique
"""


from .forms import PeriodeBilanForm  # Importez le modèle de formulaire que vous avez créé

def periode_bilan(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        
        try:
            grade=personne.grade
        except Grade.DoesNotExist:
            return HttpResponse("Grade non trouvé", status=404)
        grade_id=grade.id
        print(personne)
        print(grade_id)
        engin = Engin.objects.all()
        context = {'grade_id': grade.id, 'engin': engin, 'personne':personne, 'grade_id':grade_id}

        if request.method == 'POST':
            form = PeriodeBilanForm(request.POST)  # Créez une instance de votre modèle de formulaire

            if form.is_valid():  # Vérifiez si le formulaire est valide
                
                date_debut = form.cleaned_data['date_debut']
                date_fin = form.cleaned_data['date_fin']
                
                if date_fin < date_debut :
                    messages.error(request, "La période de fin doit être ultérieure à la période de début!")
                else:
                    engin_id = form.cleaned_data.get('engin')
                    if engin_id:
                        context['engin_id'] = engin_id
                        return redirect(reverse('administratif:bilan_partic', args=(grade.id, engin_id, date_debut, date_fin)))
                    else:
                        return redirect(reverse('administratif:bilan_glob', args=(grade.id, date_debut, date_fin)))

        else:
            form = PeriodeBilanForm()  # Créez une instance vide du formulaire pour l'affichage initial

        context['form'] = form  # Ajoutez le formulaire au contexte

        return render(request, 'periode_bilan.html', context)
    else:
        # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def bilan_periodique_glob(request, date_debut, date_fin):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)
    
        engin = Engin.objects.all()
        date_actuelle = datetime.now()
        date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d")
        context = {'grade': grade, 'date_actuelle': date_actuelle, 'grade_id': grade_id, 'date_debut': date_debut, 'date_fin': date_fin}

        try:
            maintenances = MaintenanceEngin.objects.filter(date_maint__range=[date_debut, date_fin])
            context['maintenances'] = maintenances
        except MaintenanceEngin.DoesNotExist:
            messages.error(request, "Aucune maintenance trouvée pour cette période.")

        try:
            ravitaillements = RavitaillementCarburant.objects.filter(date_rav__range=[date_debut, date_fin])
            context['ravitaillements'] = ravitaillements
        except RavitaillementCarburant.DoesNotExist:
            messages.error(request, "Aucun ravitaillement trouvé pour cette période.")

        try:
            vidanges = MaintenanceEngin.objects.filter(type_maint=4, date_maint__range=[date_debut, date_fin])
            context['vidanges'] = vidanges
        except MaintenanceEngin.DoesNotExist:
            messages.error(request, "Aucune vidange trouvée pour cette période.")

        try:
            releves = ReleveDistance.objects.filter(date_releve__range=[date_debut, date_fin])
            context['releves'] = releves
        except ReleveDistance.DoesNotExist:
            messages.error(request, "Aucun relevé de distance trouvé pour cette période.")

        nb_maintenance = maintenances.count()
        context['nb_maintenance'] = nb_maintenance
        nb_vidange = vidanges.count()
        context['nb_vidange'] = nb_vidange
        quantite_r = ravitaillements.aggregate(Sum('quantite_rav'))['quantite_rav__sum'] or 0
        context['quantite_r'] = quantite_r
        cout_m = maintenances.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        context['cout_m'] = cout_m
        cout_v = vidanges.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        context['cout_v'] = cout_v
        cout_r = ravitaillements.aggregate(Sum('cout_rav'))['cout_rav__sum'] or 0
        context['cout_r'] = cout_r
        engins_avec_notifications = Engin.objects.filter(has_notification=True)
        nb_engin_notif = engins_avec_notifications.count()
        context['nb_engin_notif'] = nb_engin_notif
        context['engins_avec_notifications'] = engins_avec_notifications

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(ravitaillements, 4)  # Nombre d'éléments par page
        try:
            ravitaillements = paginator.page(page)
        except PageNotAnInteger:
            ravitaillements = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            ravitaillements = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['ravitaillements'] = ravitaillements
        
        page = request.GET.get('page')
        paginator = Paginator(maintenances, 4)  # Nombre d'éléments par page
        try:
            maintenances = paginator.page(page)
        except PageNotAnInteger:
            maintenances = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            maintenances = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['maintenances'] = maintenances
        
        page = request.GET.get('page')
        paginator = Paginator(vidanges, 4)  # Nombre d'éléments par page
        try:
            vidanges = paginator.page(page)
        except PageNotAnInteger:
            vidanges = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            vidanges = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['vidanges'] = vidanges

        return render(request, 'bilan_periodique_glob.html', context)
    else:
        # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})


def bilan_periodique_partic(request, grade_id, engin_id, date_debut, date_fin):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)

        engin = get_object_or_404(Engin, pk=engin_id)
        date_actuelle = datetime.now()
        maintenances = []
        ravitaillements = []
        vidanges = []
        releves = []
        nb_maintenance = 0
        nb_vidange = 0
        quantite_r = 0
        cout_m = 0
        cout_v = 0
        cout_r = 0
        Km_actuel = 0
        Km_last_vidange = 0
        distance_totale = 0
        date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d")
        context = {'grade':grade, 'personne':personne, 'engin':engin, 'date_actuelle':date_actuelle, 'grade_id':grade_id, 'date_debut':date_debut, 'date_fin':date_fin}
    
        maintenances = MaintenanceEngin.objects.filter(engin_maint=engin_id, date_maint__range=[date_debut,date_fin])
        context['maintenances'] = maintenances
        
        ravitaillements = RavitaillementCarburant.objects.filter(engin_rav=engin_id, date_rav__range=[date_debut,date_fin])
        context['ravitaillements'] = ravitaillements
        
        vidanges = MaintenanceEngin.objects.filter(engin_maint=engin_id, type_maint=4,date_maint__range=[date_debut,date_fin])
        context['vidanges'] = vidanges
        
        releves = ReleveDistance.objects.all()
        context['releves'] = releves

        Km_actuel = float(releves.last().nbKmFin) if releves.exists() else 0
        context['Km_actuel'] = Km_actuel
        Km_last_vidange = float(vidanges.last().Km_vid) if vidanges.exists() else 0
        context['Km_last_vidange'] = Km_last_vidange
        
        distance_totale = Km_actuel - Km_last_vidange
        context['distance_totale'] = distance_totale
        nb_maintenance= maintenances.count()
        context['nb_maintenance'] = nb_maintenance
        nb_vidange= vidanges.count()
        context['nb_vidange'] = nb_vidange
        quantite_r = ravitaillements.aggregate(Sum('quantite_rav'))['quantite_rav__sum'] or 0
        context['quantite_r'] = quantite_r
        cout_m = maintenances.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        context['cout_m'] = cout_m
        cout_v = vidanges.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
        context['cout_v'] = cout_v
        cout_r = ravitaillements.aggregate(Sum('cout_rav'))['cout_rav__sum'] or 0
        context['cout_r'] = cout_r
        
        engins_avec_notifications = Engin.objects.filter(has_notification=True)
        nb_engin_notif = engins_avec_notifications.count()
        context['nb_engin_notif'] = nb_engin_notif
        if engins_avec_notifications.exists():
            print('notification')
        context['engins_avec_notifications'] = engins_avec_notifications
        
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(ravitaillements, 4)  # Nombre d'éléments par page
        try:
            ravitaillements = paginator.page(page)
        except PageNotAnInteger:
            ravitaillements = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            ravitaillements = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['ravitaillements'] = ravitaillements
        
        page = request.GET.get('page')
        paginator = Paginator(maintenances, 4)  # Nombre d'éléments par page
        try:
            maintenances = paginator.page(page)
        except PageNotAnInteger:
            maintenances = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            maintenances = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['maintenances'] = maintenances
        
        page = request.GET.get('page')
        paginator = Paginator(vidanges, 4)  # Nombre d'éléments par page
        try:
            vidanges = paginator.page(page)
        except PageNotAnInteger:
            vidanges = paginator.page(1)  # Afficher la première page en cas de valeur non entière
        except EmptyPage:
            vidanges = paginator.page(paginator.num_pages)  # Afficher la dernière page en cas de dépassement

        context['vidanges'] = vidanges
        
        return render(request, 'bilan_periodique_partic.html', context)
    else:
        # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

def notifications(request):
    personne_id = request.session.get('personne_id')
    if personne_id is not None:
        personne = Personne.objects.get(pk=personne_id)
        request.session['personne_id'] = personne.id
        grade=personne.grade
        grade_id=grade.id
        print(personne)
        print(grade_id)

        engins_avec_notifications = Engin.objects.filter(has_notification=True)
        msgs_notif_rav = RavitaillementCarburant.objects.filter(engin_rav__in=engins_avec_notifications)
        msgs_notif_maint = MaintenanceEngin.objects.filter(engin_maint__in=engins_avec_notifications)
        nb_engin_notif = msgs_notif_maint.count() + msgs_notif_rav.count()
        return render(request, 'notifications.html', {'engins_avec_notifications': engins_avec_notifications, 
                                                    'nb_engin_notif':nb_engin_notif, 
                                                    'grade_id':grade_id, 
                                                    'grade':grade, 
                                                    'personne':personne,
                                                    'msgs_notif_rav':msgs_notif_rav, 
                                                    'msgs_notif_maint':msgs_notif_maint})
    else:
        # Gérer le cas où personne_id n'est pas présent dans la session
        return render(request, 'erreur404.html', {'message': 'Session invalide'})

def etat_t_card(request, grade_id):
    grade = get_object_or_404(Grade, pk=grade_id)
    t_card = T_Card.objects.all()
    moto = T_Card.objects.filter(type_engin_tcard=1)
    tricycle = T_Card.objects.filter(type_engin_tcard=2)
    voiture = T_Card.objects.filter(type_engin_tcard=3)
    type_engin = TypeEngin.objects.all()
    
    nb_moto = moto.count()
    nb_tricycle = tricycle.count()
    nb_voiture = voiture.count()
    
    last_solde_moto = float(moto.last().solde) if moto.exists() else 0
    last_solde_tricycle = float(tricycle.last().solde) if tricycle.exists() else 0
    last_solde_voiture = float(voiture.last().solde) if voiture.exists() else 0