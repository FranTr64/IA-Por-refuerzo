# Generated by Django 5.1.6 on 2025-03-04 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Logica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablero',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
