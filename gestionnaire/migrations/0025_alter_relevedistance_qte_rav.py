# Generated by Django 4.2.1 on 2023-10-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0024_ravitaillementcarburant_km_plein_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relevedistance',
            name='qte_rav',
            field=models.FloatField(null=True),
        ),
    ]
