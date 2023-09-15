from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestionnaire.models import Personne,Engin,Grade

def signin(request):
    message = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                personne = Personne.objects.get(user=user)
                login(request, user)
                return redirect(reverse('administratif:espace_utilisateur', args=[personne.grade.id, user.username]))
            except Personne.DoesNotExist:
                message = 'Identifiant ou mot de passe incorrect.'
                messages.error(request, "L'utilisateur n'a pas de grade ou d'informations associées.")
                return redirect(reverse('administratif:msg_erreur') + f'?message={message}')
        else:
            try:
                my_user = User.objects.get(username=username)
                if not my_user.is_active:
                    messages.error(request, "Vous n'avez pas confirmé votre email. Veuillez le confirmer pour activer votre compte.")
                    return redirect(reverse('administratif:login'))
                else:
                    message = 'Identifiant ou mot de passe incorrect.'
                    messages.error(request, 'Mauvaise authentification')
                    return redirect(reverse('administratif:msg_erreur') + f'?message={message}')
            except User.DoesNotExist:
                message = 'Identifiant ou mot de passe incorrect.'
                return redirect(reverse('administratif:msg_erreur') + f'?message={message}')

    return render(request, 'login.html')


def signout(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect(reverse('administratif:login'))

"""
    Erreur 404
"""
def erreur_404(request):
    message = request.GET.get('message', '')
    return render(request, 'erreur404.html', {'message':message})

def espaceDeTravail(request,grade_id,username):
    context={}
    grade=get_object_or_404(Grade, pk=grade_id)
    engin=Engin.objects.all()
    context['grade_id']=grade_id
    context['grade']=grade
    context['username']=username
    context['engin']=engin
    return render(request,'espace_de_travail.html',context)