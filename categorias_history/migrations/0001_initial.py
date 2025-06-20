# Generated by Django 5.2.1 on 2025-06-09 19:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorias', '0002_alter_categorias_options_remove_categorias_codigo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('nombre_cambio', models.CharField(max_length=80)),
                ('descripcion_cambio', models.CharField(blank=True, max_length=120)),
                ('creado_fecha_cambio', models.DateTimeField()),
                ('fecha_de_modificacion_cambio', models.DateTimeField()),
                ('eliminado_cambio', models.BooleanField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to='categorias.categorias')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name_plural': 'Historial de categorías',
                'db_table': 'categorias_history',
                'ordering': ['-timestamp'],
            },
        ),
    ]
