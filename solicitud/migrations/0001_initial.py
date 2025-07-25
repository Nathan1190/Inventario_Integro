# Generated by Django 5.2.1 on 2025-07-02 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorias', '0002_alter_categorias_options_remove_categorias_codigo'),
        ('dependencias', '0001_initial'),
        ('empleados', '0007_empleados_num_identidad'),
        ('inventario', '0004_alter_stockbien_options_and_more'),
        ('subcategorias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudBien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('comentario', models.TextField(verbose_name='Motivo/Comentario')),
                ('prioridad', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], default='media', max_length=10)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('en_proceso', 'En proceso'), ('finalizada', 'Finalizada')], default='pendiente', max_length=15)),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.biennacional')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='categorias.categorias')),
                ('dependencia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dependencias.dependencias')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes_realizadas', to='empleados.empleados')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subcategorias.subcategorias')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes de Bienes',
                'ordering': ['-fecha_solicitud'],
            },
        ),
    ]
