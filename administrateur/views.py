from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from gestionnaire.models import Personne,Grade
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestionnaire.forms import PersonneForm

def CreatePersonne(request):
    if request.method == "POST":
        form=PersonneForm(request.POST)
        if form.is_valid():
            donnees=form.cleaned_data
            nom=donnees['nom']
            prenom=donnees['prenom']
            contact=donnees['contact']
            grade=donnees['grade']
            personne=Personne.objects.filter(nom=nom,prenom=prenom,contact=contact,grade=grade)
            if personne is not None:
                messages.info(request,"Cette personne existe déjà ! ")
            else:
                personne.save()
                if grade!=Grade.objects.get(id=5):  
                    return redirect ( reverse( 'administrateur:signup', args=[personne.id]))
                messages.info(request,"Succès d'enrégistrement ! ")
    else:
        form=PersonneForm()
    return render(request,'administrateur/creerPersonne.html',{'form':form})        

def signup(request,user_id):
    user = get_object_or_404(Personne, pk=user_id)
    if request.method == "POST":
        username = request.POST['username']
        firstname = user.prenom
        lastname = user.nom
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        if User.objects.filter(username=username):
            messages.error(request, 'Nom d''utilisateur déjà pris, veuillez en choisir un autre.')
            return redirect('administrateur:signup',args=[user_id])
        if User.objects.filter(email=email):
            messages.error(request, 'Cet email possède déjà un compte.')
            return redirect('administrateur:signup',args=[user_id])
        if len(username)>10:
            messages.error(request, 'Le nom d''utilisateur ne doit pas excéder 10 caractères.')
            return redirect('administrateur:signup',args=[user_id])
        if len(username)<5:
            messages.error(request, 'Le nom d''utilisateur ne doit pas être en dessous de 5 caractères.')
            return redirect('administrateur:signup',args=[user_id])
        if not username.isalnum():
            messages.error(request, 'Le nom d''utilisateur doit être alphanumeric, c''est à dire composé de chiffres et de lettres')
            return redirect('administrateur:signup',args=[user_id])

        if password != confirmpwd:
            messages.error(request, 'Mot de passe non identique! ')  
            return redirect('administrateur:signup',args=[user_id])                  

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        messages.success(request, 'Le compte a été créé avec succès.')
    return render(request, 'administrateur/creerUtilisateur.html')    
