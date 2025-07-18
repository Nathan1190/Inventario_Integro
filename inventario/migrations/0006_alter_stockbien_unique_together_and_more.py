# Generated by Django 5.2.1 on 2025-07-03 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0002_alter_categorias_options_remove_categorias_codigo'),
        ('inventario', '0005_biennacional_objeto_gasto'),
        ('objeto_gasto', '0001_initial'),
        ('subcategorias', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stockbien',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='stockbien',
            name='objeto_gasto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='objeto_gasto.objetogasto'),
        ),
        migrations.AlterUniqueTogether(
            name='stockbien',
            unique_together={('nombre_bien', 'objeto_gasto', 'categoria', 'subcategoria')},
        ),
    ]
