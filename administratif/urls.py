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
    path('espace/utilisateur/<int:grade_id>', views.espaceDeTravail, name='espace_utilisateur'),
# Erreur 404
    path('erreur_404/',views.erreur_404, name='msg_erreur'),
# Analyses
    path('analyse_globales/<int:grade_id>/<str:type_bilan>', views.analyse_glob, name='analyses_glob'),
    path('analyse_particulieres/<int:grade_id>/<int:engin_id>/<str:type_bilan>', views.analyse_partic,\
        name='analyses_partic'),
    path('periode_bilan/<int:grade_id>/<str:type_bilan>', views.periode_bilan,\
        name='periode_bilan'),
    path('bilan_periodique_general/<int:grade_id>/<str:type_bilan>/<int:day_1>/<int:month_1>/<int:year_1>/<int:day_2>/<int:month_2>/<int:year_2>', views.bilan_periodique_glob,\
        name='bilan_glob'),
    path('bilan_periodique_particulier/<int:grade_id>/<int:engin_id>/<str:type_bilan>/<int:day_1>/<int:month_1>/<int:year_1>/<int:day_2>/<int:month_2>/<int:year_2>', \
        views.bilan_periodique_partic, name='bilan_partic')    
]