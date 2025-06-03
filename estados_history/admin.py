from django.contrib import admin
from .models import Estados_History

@admin.register(Estados_History)
class EstadosAdmin(admin.ModelAdmin):
    list_display      = ('estado', 'timestamp', 'changed_by', 'nombre_cambio', 'color_hex_cambio', 'descripcion_cambio', 'eliminado_cambio', 'creado_en_cambio', 'actualizado_en_cambio')
    list_filter       = ('eliminado_cambio',)
    search_fields     = ('timestamp',)
