# Generated by Django 4.2.1 on 2023-10-31 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0035_t_card_montant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ravitaillementcarburant',
            name='Km_plein',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ravitaillementcarburant',
            name='conso',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ravitaillementcarburant',
            name='plein',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
