# Generated by Django 4.2.1 on 2023-08-11 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personne',
            old_name='grade_user',
            new_name='grade',
        ),
        migrations.AlterField(
            model_name='grade',
            name='libelle_grade',
            field=models.CharField(max_length=50),
        ),
    ]
