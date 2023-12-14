from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'administratif'
# def protected_path(route, view, kwargs=None, name=None):
#     return path(route, login_required(view), kwargs=kwargs, name=name)

urlpatterns = [
#Login
    path('',views.signin,name='login'),
# Logout
    path('deconnexion/',views.signout,name='logout'),
# Espaces de travail
    path('espace/utilisateur/', views.espaceDeTravail, name='espace_utilisateur'),
# Erreur 404
    path('erreur_404/',views.erreur_404, name='msg_erreur'),
# Analyses
    path('analyse_globales/', views.analyse_glob, name='analyses_glob'),
    path('analyse_particulieres/<int:engin_id>', views.analyse_partic,\
        name='analyses_partic'),
    path('periode_bilan/', views.periode_bilan,\
        name='periode_bilan'),
    path(
    'bilan_periodique_general/<str:date_debut>/<str:date_fin>/',
    views.bilan_periodique_glob,
    name='bilan_glob'),
    path('bilan_periodique_particulier/<int:engin_id>/<str:date_debut>/<str:date_fin>/',
        views.bilan_periodique_partic, name='bilan_partic'), 
    path('notifications/', views.notifications, name='notifications'),
    
]