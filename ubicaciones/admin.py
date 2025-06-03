from django.contrib import admin
from .models import Ubicaciones

@admin.register(Ubicaciones)
class UbicacionesAdmin(admin.ModelAdmin):
    list_display      = ('id', 'nombre', 'descripcion', 'activo', 'creado_fecha', 'fecha_de_modificacion', 'eliminado')
    list_filter       = ('eliminado', 'activo')
    search_fields     = ('nombre','activo')
