# Generated by Django 4.2.1 on 2023-09-01 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0012_alter_personne_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='relevedistance',
            name='distance',
            field=models.FloatField(default=0),
        ),
    ]
