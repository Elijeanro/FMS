# Generated by Django 4.2.1 on 2023-08-19 05:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0008_alter_attribution_date_attribution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='engin',
            name='date_creation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
