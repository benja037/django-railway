# Generated by Django 5.0.6 on 2024-07-23 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_alter_fbrefstatsjugador_ast_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbrefstatsjugador',
            name='equipo',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.equipo'),
        ),
    ]
