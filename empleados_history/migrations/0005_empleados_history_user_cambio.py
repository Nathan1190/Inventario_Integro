# Generated by Django 5.2.1 on 2025-07-02 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados_history', '0004_empleados_history_numero_identidad_cambio'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleados_history',
            name='user_cambio',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
