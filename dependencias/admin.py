from django.contrib import admin
from .models import Dependencias

@admin.register(Dependencias)
class DependenciasAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'descripcion',
        'eliminado',
        'creado_fecha',
        'fecha_de_modificacion',
    )
    list_filter = ('eliminado',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('id',)
    readonly_fields = ('creado_fecha', 'fecha_de_modificacion')

    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'eliminado')
        }),
        ('Fechas', {
            'fields': ('creado_fecha', 'fecha_de_modificacion'),
            'classes': ('collapse',),
        }),
    )