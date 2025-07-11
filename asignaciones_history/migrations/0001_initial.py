# Generated by Django 5.2.1 on 2025-06-30 17:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asignaciones', '0001_initial'),
        ('empleados', '0006_empleados_codigo_empleado_empleados_correo_inst'),
        ('inventario', '0004_alter_stockbien_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignaciones_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=20)),
                ('fecha_asignacion', models.DateTimeField()),
                ('fecha_firma', models.DateTimeField(blank=True, null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('cambiado_en', models.DateTimeField(auto_now_add=True)),
                ('asignacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignaciones.asignacionbien')),
                ('asignado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_hechas', to=settings.AUTH_USER_MODEL)),
                ('bien', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.biennacional')),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignacion_cambios', to=settings.AUTH_USER_MODEL)),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='empleados.empleados')),
            ],
        ),
    ]
