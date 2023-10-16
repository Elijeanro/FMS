from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from gestionnaire.models import Personne,Engin,Grade,Marque,Modele,TypeEngin,Fournisseur,MaintenanceEngin,RavitaillementCarburant,ReleveDistance

# nb_a_ravitailler= RavitaillementCarburant.objects.filter(infoligne_id__in=infln_ids, etat_billet=2).count()

def signin(request):
    message = ''
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        context['user'] = user
        if user is not None:
            try:
                personne = Personne.objects.get(utilisateur=user)
                login(request, user)
                return redirect(reverse('administratif:espace_utilisateur', args=[personne.grade.id]))
            except Personne.DoesNotExist:
                message = 'Identifiant ou mot de passe incorrect!'
                messages.error(request, "Mauvaise authentification!")
                return redirect(reverse('administratif:msg_erreur') + f'?message={message}')
        else:
            try:
                my_user = User.objects.get(username=username)
                if not my_user.is_active:
                    message = 'Une erreur est survenue, veuillez reprendre!'
                    messages.error(request, "Vous n'avez pas confirmé votre email. Veuillez le confirmer pour activer votre compte!")
                    return redirect(reverse('administratif:msg_erreur'))
                else:
                    messages.error(request, 'Identifiant ou mot de passe incorrect!')
                    return redirect(reverse('administratif:login') + f'?message={message}')
            except User.DoesNotExist:
                messages.error(request, 'Identifiant ou mot de passe incorrect!')
                return redirect(reverse('administratif:login') + f'?message={message}')

    return render(request, 'login.html',context)


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
def espaceDeTravail(request, grade_id):
    context = {}
    grade = get_object_or_404(Grade, pk=grade_id)
    engin = Engin.objects.all()
    context['grade_id'] = grade_id
    context['grade'] = grade
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
        elif num_objet == 4 :
            valeur = Modele.objects.filter(nom_modele__icontains=chaine).values_list('id',flat=True)
            resultat = Engin.objects.filter(modele_engin__in=valeur)
        elif num_objet == 5 :
            valeur = TypeEngin.objects.filter(designation__icontains=chaine).values_list('id',flat=True)
            resultat = Engin.objects.filter(type_engin__in=valeur)
        elif num_objet == 6 :
            valeur = Fournisseur.objects.filter(nom_fournisseur__icontains=chaine).values_list('id',flat=True)
            resultat = Engin.objects.filter(fournisseur_engin__in=valeur)
        else : 
            resultat = engin

        context['engin'] = resultat

    return render(request, 'espace_de_travail.html', context)

"""
    Les analyses
"""
# def analyse_glob(request, grade_id, type_bilan):
#     grade = get_object_or_404(Grade, pk=grade_id)
#     maintenances = MaintenanceEngin.objects.all()
#     ravitaillements = RavitaillementCarburant.objects.all()
#     vidanges = MaintenanceEngin.objects.filter(type_maint=4)
#     releves = ReleveDistance.objects.all()
    
#     nb_maintenance= maintenances.count()
#     nb_vidange= vidanges.count()
#     quantite_r = ravitaillements.aggregate(Sum('quantite_rav'))['quantite_rav__sum'] or 0
#     cout_m = maintenances.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
#     cout_v = vidanges.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
#     cout_r = ravitaillements.aggregate(Sum('cout_rav'))['cout_rav__sum'] or 0
    
    
#     context = {
#         'grade':grade,
#         'grade_id':grade_id,
#         'maintenances':maintenances,
#         'ravitaillements':ravitaillements,
#         'quantite_rav':quantite_r,
#         'nb_maintenance':nb_maintenance,
#         'nb_vidange':nb_vidange,
#         'vidanges':vidanges,
#         'releves':releves,
#         'cout_m':cout_m,
#         'cout_r':cout_r,
#         'cout_v':cout_v,
#         'type_bilan':type_bilan,
#     }
#     return render(request,'analyse/analyses_glob.html',context)

def analyse_glob(request, grade_id, type_bilan):
    grade = get_object_or_404(Grade, pk=grade_id)
    maintenances = MaintenanceEngin.objects.all()
    ravitaillements = RavitaillementCarburant.objects.all()
    vidanges = MaintenanceEngin.objects.filter(type_maint=4)
    releves = ReleveDistance.objects.all()

    ravitaillements = RavitaillementCarburant.objects.all().order_by('date_rav')

    # Initialisation de la variable pour stocker les données d'écart de consommation
    ecart_conso_data = []

    prev_ravitaillement = None

    for ravitaillement in ravitaillements:
        if prev_ravitaillement:
            ecart = (ravitaillement.Km_plein - prev_ravitaillement.Km_plein)
            ecart_conso = ((ravitaillement.quantite_rav * 100 / ecart) - ravitaillement.engin_rav.info_engin.consommation) * 100
        else:
            ecart_conso = 0  # Aucun ravitaillement précédent, définir l'écart à 0

        ecart_conso_data.append(ecart_conso)
        prev_ravitaillement = ravitaillement

    # Attachez les données d'écart de consommation à chaque ravitaillement
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
        'maintenances': maintenances,
        'ravitaillements': ravitaillements,
        'quantite_rav': quantite_r,
        'nb_maintenance': nb_maintenance,
        'nb_vidange': nb_vidange,
        'vidanges': vidanges,
        'releves': releves,
        'cout_m': cout_m,
        'cout_r': cout_r,
        'cout_v': cout_v,
        'type_bilan': type_bilan,
    }
    return render(request, 'analyse/analyses_glob.html', context)


def analyse_partic(request, grade_id, engin_id, type_bilan):
    grade = get_object_or_404(Grade, pk=grade_id)
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
        'type_bilan':type_bilan,
    }
    return render(request, 'analyse/analyses_partic.html', context)


"""
    Le bilan périodique
"""
def periode_bilan(request, grade_id, type_bilan):
    try:
        grade = get_object_or_404(Grade, pk=grade_id)
    except Grade.DoesNotExist:
        return HttpResponse("Grade non trouvé", status=404)

    engin = Engin.objects.all()
    
    context = {'type_bilan': type_bilan}
    context['grade_id'] = grade.id
    context['engin'] = engin
    
    if request.method == 'POST':
        day_1 = int(request.POST.get('jour_1'))
        context['day_1'] = day_1
        month_1 = int(request.POST.get('mois_1'))
        context['month_1'] = month_1
        year_1 = int(request.POST.get('annee_1'))
        context['year_1'] = year_1
        
        day_2 = int(request.POST.get('jour_2'))
        context['day_2'] = day_2
        month_2 = int(request.POST.get('mois_2'))
        context['month_2'] = month_2
        year_2 = int(request.POST.get('annee_2'))
        context['year_2'] = year_2

        if year_2 < year_1 or (year_2 == year_1 and month_2 < month_1):
            messages.error(request, "La période de fin doit être ultérieure à la période de début!")
        else:
            pass

        # Vérifiez si 'engin' a été renseigné dans le formulaire
        engin_id = request.POST.get('engin', None)
        if request.POST.get('engin'):
            engin_id = request.POST.get('engin')
            context['engin_id'] = engin_id
            return redirect(reverse('administratif:bilan_partic', args=(grade.id, engin_id, type_bilan, day_1, month_1, year_1, day_2, month_2, year_2)))
        else:
            return redirect(reverse('administratif:bilan_glob', args=(grade.id, type_bilan, day_1, month_1, year_1, day_2, month_2, year_2)))
    return render(request, 'periode_bilan.html', context)


def bilan_periodique_glob(request, grade_id, type_bilan, day_1, month_1, year_1, day_2, month_2, year_2):
    grade = get_object_or_404(Grade, pk=grade_id)
    grade_id = grade.id
    engin = Engin.objects.all()
    date_actuelle = datetime.now()
    context = {'grade':grade, 'engin':engin, 'date_actuelle':date_actuelle, 'grade_id':grade_id, 'day_1':day_1, 'month_1':month_1, 'year_1':year_1, 'day_2':day_2, 'month_2':month_2, 'year_2':year_2}
    
    try:
        maintenances = MaintenanceEngin.objects.filter(date_maint__range=[
            datetime(year_1, month_1, day_1),
            datetime(year_2, month_2, day_2)
        ])
        context['maintenances'] = maintenances
    except MaintenanceEngin.DoesNotExist:
        messages.error(request, "Aucune maintenance trouvée pour cette période.")
    
    try:
        ravitaillements = RavitaillementCarburant.objects.filter(date_rav__range=[
            datetime(year_1, month_1, day_1),
            datetime(year_2, month_2, day_2)
        ])
        context['ravitaillements'] = ravitaillements
    except RavitaillementCarburant.DoesNotExist:
        messages.error(request, "Aucun ravitaillement trouvé pour cette période.")
    
    try:
        vidanges = MaintenanceEngin.objects.filter(type_maint=4, date_maint__range=[
            datetime(year_1, month_1, day_1),
            datetime(year_2, month_2, day_2)
        ])
        context['vidanges'] = vidanges
    except MaintenanceEngin.DoesNotExist:
        messages.error(request, "Aucune vidange trouvée pour cette période.")
    
    try:
        releves = ReleveDistance.objects.filter(date_releve__range=[
            datetime(year_1, month_1, day_1),
            datetime(year_2, month_2, day_2)
        ])
        context['releves'] = releves
    except ReleveDistance.DoesNotExist:
        messages.error(request, "Aucun relevé de distance trouvé pour cette période.")
    
    type_bilan = 'options'
    nb_maintenance = maintenances.count()
    context['nb_maintenance'] = nb_maintenance
    nb_vidange = vidanges.count()
    context['nb_vidange'] = nb_vidange
    quantite_r = ravitaillements.aggregate(Sum('quantite_rav'))['quantite_rav__sum'] or 0
    context['quantite_r'] = quantite_r
    cout_m = maintenances.aggregate(Sum('cout_maint'))['cout_maint__sum'] or 0
    context['cout_m'] = cout_m
    cout_v = ravitaillements.aggregate(Sum('cout_rav'))['cout_rav__sum'] or 0
    context['cout_v'] = cout_v
    cout_r = ravitaillements.aggregate(Sum('cout_rav'))['cout_rav__sum'] or 0
    context['cout_r'] = cout_r
    context['type_bilan'] = type_bilan

    return render(request, 'bilan_periodique_glob.html', context)

def bilan_periodique_partic(request, grade_id, engin_id,type_bilan, day_1, month_1, year_1, day_2, month_2, year_2):
    grade = get_object_or_404(Grade, pk=grade_id)
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
    context = {'grade':grade, 'engin':engin, 'date_actuelle':date_actuelle, 'grade_id':grade_id, 'day_1':day_1, 'month_1':month_1, 'year_1':year_1, 'day_2':day_2, 'month_2':month_2, 'year_2':year_2}
   
    maintenances = MaintenanceEngin.objects.filter(engin_maint=engin_id, date_maint__range=[\
            datetime(year=year_1, month=month_1, day=day_1 ), \
            datetime(year=year_2, month=month_2, day=day_2 )\
                ])
    context['maintenances'] = maintenances
    
    ravitaillements = RavitaillementCarburant.objects.filter(engin_rav=engin_id, date_rav__range=[\
            datetime(year=year_1, month=month_1, day=day_1 ), \
            datetime(year=year_2, month=month_2, day=day_2 )\
                ])
    context['ravitaillements'] = ravitaillements
    
    vidanges = MaintenanceEngin.objects.filter(engin_maint=engin_id, type_maint=4,date_maint__range=[\
            datetime(year=year_1, month=month_1, day=day_1 ), \
            datetime(year=year_2, month=month_2, day=day_2 )\
                ])
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
    context['type_bilan'] = type_bilan

    return render(request, 'bilan_periodique_partic.html', context)