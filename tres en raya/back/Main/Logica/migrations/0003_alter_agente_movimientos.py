# Generated by Django 5.1.6 on 2025-03-04 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Logica', '0002_tablero_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agente',
            name='movimientos',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
