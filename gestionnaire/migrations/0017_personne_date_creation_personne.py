# Generated by Django 4.2.1 on 2023-09-29 06:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0016_alter_maintenanceengin_motif_maint'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='date_creation_personne',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
