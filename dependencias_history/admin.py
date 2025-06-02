from django.contrib import admin
from .models import Dependencias_History

# Register your models here.
@admin.register(Dependencias_History)
class DependenciasHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dependencia',
        'changed_by',
        'timestamp',
        'nombre_cambio',
        'descripcion_cambio',
        'eliminado_cambio',
        'creado_fecha_cambio',
        'fecha_de_modificacion_cambio',
    )
    list_filter = ('changed_by', 'eliminado_cambio')
    search_fields = ('dependencia__nombre', 'nombre_cambio', 'descripcion_cambio')
    ordering = ('-timestamp',)
    readonly_fields = (
        'dependencia',
        'changed_by',
        'timestamp',
        'nombre_cambio',
        'descripcion_cambio',
        'eliminado_cambio',
        'creado_fecha_cambio',
        'fecha_de_modificacion_cambio',
    )

    