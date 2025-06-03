from django.contrib import admin
from .models import Proveedores

@admin.register(Proveedores)
class ProveedoresAdmin(admin.ModelAdmin):
    list_display      = ('id', 'nombre', 'descripcion', 'telefono', 'correo', 'direccion', 'activo', 'creado_fecha', 'fecha_de_modificacion', 'eliminado')
    list_filter       = ('eliminado', 'activo')
    search_fields     = ('nombre','activo')
