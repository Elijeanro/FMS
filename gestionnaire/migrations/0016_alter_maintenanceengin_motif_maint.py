# Generated by Django 4.2.1 on 2023-09-26 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0015_remove_personne_user_utilisateur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenanceengin',
            name='motif_maint',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
