# Generated by Django 4.2.1 on 2023-10-15 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionnaire', '0030_engin_vik'),
    ]

    operations = [
        migrations.AddField(
            model_name='engin',
            name='capa_reserv',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='relevedistance',
            name='ravitaillement',
            field=models.BooleanField(default=False, null=True),
        ),
    ]