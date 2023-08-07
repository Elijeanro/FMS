from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from gestionnaire.models import Utilisateur,TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,VidangeEngin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance
from .forms import LoginForm

""" 
Page d'authentification
"""
def LoginView(request):
    message = ''
    context={}
    if request.method == 'POST':
        connexion = LoginForm(request.POST)
        
        if connexion.is_valid():
            donnees = connexion.cleaned_data
            username = donnees['email']
            password = donnees['motDePasse']
            user = Utilisateur.objects.filter(personne__email=username, motDePasse=password).first()
            context['form'] = connexion
            
            if user is not None :
                user_grade = user.grade_user.id
                if user_grade == 1234567890: 
                    return redirect(reverse('gestionnaire:espace_dg', args=[user.personne.id]))
                if user_grade == 1:
                    return redirect(reverse('gestionnaire:espace_gestionnaire', args=[user.personne.id]))
                elif user_grade == 2: 
                    return redirect(reverse('public:espace_utilisateur', args=[user.personne.id]))
                else:
                    message = "Grade inconnu."
                    return redirect(reverse('public:msg_erreur') + f'?message={message}')
            else:
                message = 'Identifiant ou mot de passe incorrect.'
                return redirect(reverse('public:msg_erreur') + f'?message={message}')
        else:
            context['form'] = connexion
    else:
        connexion = LoginForm()
        
    context['form'] = connexion
    return render(request, 'login.html',context)

"""
 Espace de travail de l'utilisateur
"""
def EspaceUserView(request,id_user):
    context = {}
    user = get_object_or_404(Utilisateur, pk=id_user)
    return render(request, 'public/espace_utilisateur.html', context)

"""
    Erreur 404
"""
def erreur_404(request):
    message = request.GET.get('message', '')
    return render(request, 'erreur404.html', {'message':message})