from django.contrib import admin
from gestionnaire.models import Utilisateur,TypeEngin,TypeMaintenance,Grade,InfoEngin,Engin,VidangeEngin,\
    MaintenanceEngin,Marque,Modele,Personne,RavitaillementCarburant,ReleveDistance

admin.site.register(Utilisateur)
admin.site.register(TypeEngin)
admin.site.register(TypeMaintenance)
admin.site.register(Grade)
admin.site.register(InfoEngin)
admin.site.register(Engin)
admin.site.register(VidangeEngin)
admin.site.register(MaintenanceEngin)
admin.site.register(Marque)
admin.site.register(Personne)
admin.site.register(Modele)
admin.site.register(RavitaillementCarburant)
admin.site.register(ReleveDistance)
