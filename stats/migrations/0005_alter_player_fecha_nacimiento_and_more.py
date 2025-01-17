# Generated by Django 5.0.6 on 2024-07-20 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_sofascorestatsjugador_equipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='fecha_nacimiento',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='nacionalidad',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='nombre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='posicion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
