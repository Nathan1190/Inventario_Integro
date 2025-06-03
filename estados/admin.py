from django.contrib import admin
from .models import Estados

@admin.register(Estados)
class EstadosAdmin(admin.ModelAdmin):
    list_display      = ('id', 'nombre', 'color_hex', 'descripcion', 'eliminado', 'creado_en', 'actualizado_en')
    list_filter       = ('eliminado',)
    search_fields     = ('nombre','color_hex')
