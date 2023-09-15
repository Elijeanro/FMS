from django.contrib import admin
from django.urls import path
from . import views

app_name = 'administratif'
urlpatterns = [
#Login
    path('',views.signin,name='login'),
# Logout
    path('deconnexion',views.signout,name='logout'),
# Espaces de travail
    path('espace/utilisateur/<int:grade_id>/<str:username>/', views.espaceDeTravail, name='espace_utilisateur'),
# Erreur 404
    path('erreur_404/',views.erreur_404, name='msg_erreur'),
    
]