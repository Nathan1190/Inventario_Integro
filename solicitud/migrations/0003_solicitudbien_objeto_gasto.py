# Generated by Django 5.2.1 on 2025-07-03 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objeto_gasto', '0001_initial'),
        ('solicitud', '0002_solicitudbien_memo'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudbien',
            name='objeto_gasto',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='objeto_gasto.objetogasto'),
            preserve_default=False,
        ),
    ]
