from django.contrib import admin
from django.urls import path
from . import views

app_name = 'administrateur'
urlpatterns = [
# Créer des profils
    path('fms/signup/<str:sujet>',views.CreatePersonne,name='creerpersonne'),
    path('fms/signup/<int:personne_id>/<str:sujet>',views.signup,name='signup'),
    path('fms/creer_grade',views.create_grade,name='create_grade'),
]