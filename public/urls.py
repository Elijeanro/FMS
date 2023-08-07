from django.contrib import admin
from django.urls import path
from . import views

app_name = 'public'
urlpatterns = [
    # Login
    path('',views.LoginView,name='login'),
    # Espaces de travail
    path('espace/utilisateur/<int:id_user>',views.EspaceUserView,name='espace_utilisateur'),
    # Erreur 404
    path('erreur_404/',views.erreur_404, name='msg_erreur'),
    
]