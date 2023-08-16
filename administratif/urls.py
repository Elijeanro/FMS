from django.contrib import admin
from django.urls import path
from . import views

app_name = 'administratif'
urlpatterns = [
#Login
    path('',views.signin,name='login'),
# Espaces de travail
    path('espace/utilisateur/',views.espaceDeTravail,name='espace_utilisateur'),
# Erreur 404
    path('erreur_404/',views.erreur_404, name='msg_erreur'),
    
]