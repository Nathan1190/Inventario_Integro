from django.contrib import admin
from .models import Cargos_History

@admin.register(Cargos_History)
class Cargos_HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cargo', 'changed_by', 'timestamp', 'nombre_cambio', 'descripcion_cambio', 'eliminado_cambio', 'creado_fecha_cambio', 'fecha_de_modificacion_cambio')
    list_filter = ('eliminado_cambio', 'creado_fecha_cambio', 'fecha_de_modificacion_cambio', 'changed_by')
    search_fields = ('nombre_cambio', 'descripcion_cambio')
    ordering = ('id',)
    date_hierarchy = 'creado_fecha_cambio'

