# Generated by Django 4.2.1 on 2023-10-05 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0019_personne_utilisateur_delete_utilisateur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vidangeengin',
            name='maint_vid',
        ),
        migrations.AddField(
            model_name='vidangeengin',
            name='Km_vid',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vidangeengin',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]