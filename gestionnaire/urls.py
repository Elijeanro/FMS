from django.contrib import admin
from django.urls import path
from . import views

app_name = 'gestionnaire'
urlpatterns = [
# URLs principales
    path('creation/<str:sujet>/', views.creation, name='creation'),
    path('delete/<str:sujet>/', views.delete, name='delete'),
    path('details/<int:pk>/<str:sujet>/', views.details, name='details'),
    path('lists/<str:sujet>/', views.lists, name='lists'),
    path('results/<str:sujet>/', views.results, name='results'),
    path('update/<str:sujet>/', views.update, name='update'),
    
# Les créations
    path('create/personne/', views.create_personne, name='create_personne'),
    path('create/marque/', views.create_marque, name='create_marque'),
    path('create/modele/', views.create_modele, name='create_modele'),
    path('create/fournisseur/', views.create_fournisseur, name='create_fournisseur'),
    path('create/engin/', views.create_engin, name='create_engin'),
    path('create/type-engin/', views.create_type_engin, name='create_type_engin'),
    path('create/etat-engin/', views.create_etat_engin, name='create_etat_engin'),
    path('create/info-engin/', views.create_info_engin, name='create_info_engin'),
    path('create/ravitaillement-carburant/', views.create_ravitaillement_carburant, name='create_ravitaillement_carburant'),
    path('create/vidange-engin/', views.create_vidange_engin, name='create_vidange_engin'),
    path('create/type-maintenance/', views.create_type_maintenance, name='create_type_maintenance'),
    path('create/maintenance-engin/', views.create_maintenance_engin, name='create_maintenance_engin'),
    path('create/attribution/', views.create_attribution, name='create_attribution'),
    path('create/releve-distance/', views.create_releve_distance, name='create_releve_distance'),
    
# Les Modifications
    path('update/personne/<int:pk>/', views.update_personne, name='update_personne'),
    path('update/type-engin/<int:pk>/', views.update_type_engin, name='update_type_engin'),
    path('update/modele/<int:pk>/', views.update_modele, name='update_modele'),
    path('update/fournisseur/<int:pk>/', views.update_fournisseur, name='update_fournisseur'),
    path('update/info-engin/<int:pk>/', views.update_info_engin, name='update_info_engin'),
    path('update/ravitaillement-carburant/<int:pk>/', views.update_ravitaillement_carburant, name='update_ravitaillement_carburant'),
    path('update/engin/<int:pk>/', views.update_engin, name='update_engin'),
    path('update/marque/<int:pk>/', views.update_marque, name='update_marque'),
    path('update/etat-engin/<int:pk>/', views.update_etat_engin, name='update_etat_engin'),
    path('update/vidange-engin/<int:pk>/', views.update_vidange_engin, name='update_vidange_engin'),
    path('update/maintenance-engin/<int:pk>/', views.update_maintenance_engin, name='update_maintenance_engin'),
    path('update/type-maintenance/<int:pk>/', views.update_type_maintenance, name='update_type_maintenance'),
    path('update/attribution/<int:pk>/', views.update_attribution, name='update_attribution'),
    path('update/releve-distance/<int:pk>/', views.update_releve_distance, name='update_releve_distance'),

# Les Suppressions
    path('delete/modele/<int:modele_id>/', views.delete_modele, name='delete_modele'),
    path('delete/info-engin/<int:info_engin_id>/', views.delete_info_engin, name='delete_info_engin'),
    path('delete/ravitaillement-carburant/<int:ravitaillement_carburant_id>/', views.delete_ravitaillement_carburant, name='delete_ravitaillement_carburant'),
    path('delete/personne/<int:personne_id>/', views.delete_personne, name='delete_personne'),
    path('delete/marque/<int:marque_id>/', views.delete_marque, name='delete_marque'),
    path('delete/fournisseur/<int:fournisseur_id>/', views.delete_fournisseur, name='delete_fournisseur'),
    path('delete/engin/<int:engin_id>/', views.delete_engin, name='delete_engin'),
    path('delete/type-engin/<int:type_engin_id>/', views.delete_type_engin, name='delete_type_engin'),
    path('delete/etat-engin/<int:etat_engin_id>/', views.delete_etat_engin, name='delete_etat_engin'),
    path('delete/vidange-engin/<int:vidange_engin_id>/', views.delete_vidange_engin, name='delete_vidange_engin'),
    path('delete/type-maintenance/<int:type_maintenance_id>/', views.delete_type_maintenance, name='delete_type_maintenance'),
    path('delete/maintenance-engin/<int:maintenance_engin_id>/', views.delete_maintenance_engin, name='delete_maintenance_engin'),
    path('delete/attribution/<int:attribution_id>/', views.delete_attribution, name='delete_attribution'),
    path('delete/releve-distance/<int:releve_distance_id>/', views.delete_releve_distance, name='delete_releve_distance'),

]