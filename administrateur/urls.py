from django.contrib import admin
from django.urls import path
from . import views

app_name = 'administrateur'
urlpatterns = [
# Espaces de travail
    # path('espace/Gestionnaire/<int:id_ges>',views.EspaceGestionnaireView,name='espace_ges'),
# Créer des profils
    path('fms/signup/',views.CreatePersonne,name='creerpersonne'),
    path('fms/signup/<int:user_id>',views.signup,name='signup'),
    
]