# Generated by Django 4.2.1 on 2023-10-28 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0034_t_card_approvisionnement'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_card',
            name='montant',
            field=models.FloatField(default=0.0),
        ),
    ]