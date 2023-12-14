from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from gestionnaire.models import Personne,Grade
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestionnaire.forms import PersonneForm
from .forms import GradeForm
from django.contrib.auth.decorators import login_required


def CreatePersonne(request,sujet):
    sujet='personne'
    print('ouverture de la page')
    if request.method == "POST":
        print('vérification de la methode POST')
        form=PersonneForm(request.POST)
        if form.is_valid():
            print('vérification du formulaire')
            donnees=form.cleaned_data
            nom=donnees['nom']
            prenom=donnees['prenom']
            contact=donnees['contact']
            grade=donnees['grade']
            grade = Grade.objects.get(id=grade)
            print('recherche d''une personne existante')
            personne=Personne.objects.filter(nom=nom,prenom=prenom,contact=contact,grade=grade)
            if personne:
                print('si cette personne existe déjà dans la base, envoyer un message')
                messages.info(request,"Cette personne existe déjà ! ")
            else:
                print('si cette personne n''existe pas encore dans la base, procéder à l''enregistrement')
                personne = Personne(
                    nom=nom,
                    prenom=prenom,
                    contact=contact,
                    grade=grade,
                )
                personne.save()
                print('Enregistré dans la base')
                personne_id = personne.id
                if grade!=Grade.objects.get(id=5): 
                    sujet='utilisateur' 
                    return redirect(reverse('administrateur:signup', args=[personne_id,sujet]))
                messages.info(request,"Succès d'enrégistrement ! ")
    else:
        form=PersonneForm()
    return render(request,'administrateur/creerPersonne.html',{'form':form, 'sujet':sujet})

def signup(request,personne_id,sujet):
    user = get_object_or_404(Personne, pk=personne_id)
    if request.method == "POST":
        username = request.POST['username']
        firstname = user.prenom
        lastname = user.nom
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        if User.objects.filter(username=username):
            messages.error(request, 'Nom d''utilisateur déjà pris, veuillez en choisir un autre.')
            return redirect(reverse('administrateur:signup',args=[personne_id,sujet]))
        if User.objects.filter(email=email):
            messages.error(request, 'Cet email possède déjà un compte.')
            return redirect(reverse('administrateur:signup',args=[personne_id,sujet]))
        if len(username)>10:
            messages.error(request, 'Le nom d''utilisateur ne doit pas excéder 10 caractères.')
            return redirect(reverse('administrateur:signup',args=[personne_id,sujet]))
        if len(username)<5:
            messages.error(request, 'Le nom d''utilisateur ne doit pas être en dessous de 5 caractères.')
            return redirect(reverse('administrateur:signup',args=[personne_id,sujet]))
        if not username.isalnum():
            messages.error(request, 'Le nom d''utilisateur doit être alphanumeric, c''est à dire composé de chiffres et de lettres')
            return redirect(reverse('administrateur:signup',args=[personne_id,sujet]))

        if password != confirmpwd:
            messages.error(request, 'Mot de passe non identique! ')  
            return redirect(reverse('administrateur:signup',args=[personne_id,sujet]))                  

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        messages.success(request, 'Le compte a été créé avec succès.')
        return redirect('gestionnaire:details',args=[personne_id,sujet])
    return render(request, 'administrateur/creerUtilisateur.html', {'user':user})    

def create_grade(request):
    sujet = 'grade'
    
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            libelle_grade = form.cleaned_data['libelle_grade']
            existing_grade = Grade.objects.filter(libelle_grade=libelle_grade).first()
            if existing_grade:
                messages.error(request, 'Un grade avec ce libelle existe déjà.')
            else:
                grade=grade(
                    libelle_grade=libelle_grade,
                )
                grade.save()
                return redirect(reverse('gestionnaire:details',args=[grade.id, sujet]))  
    else:
        form = GradeForm()
        
    return render(request, 'gestionnaire/creation.html', {'form': form, 'sujet': sujet})