from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'espace_de_travail.html', {"firstname": firstname})
        else:
            try:
                my_user = User.objects.get(username=username)
                if my_user.is_active == False:
                    messages.error(request, 'You have not confirmed your email. Please confirm it to activate your account.')
                    return redirect(reverse('administratif:login'))
                else:
                    messages.error(request, 'Bad authentication')
                    return redirect('administratif:msg_erreur')
            except User.DoesNotExist:
                return redirect('administratif:msg_erreur')

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

def espaceDeTravail(request):
    return render(request,'espace_de_travail.html')