# Generated by Django 5.2.1 on 2025-05-29 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargos', '0001_initial'),
        ('empleados', '0003_alter_empleados_cargo_alter_empleados_contacto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleados',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cargos.cargos'),
        ),
    ]
