from django.contrib import admin
from .models import Empleados_History

@admin.register(Empleados_History)
class RolesAdmin(admin.ModelAdmin):
    list_display      = ('empleado', 'timestamp', 'nombre_cambio', 'cargo_cambio', 'dependencia_cambio', 'contacto_cambio', 'activo_cambio', 'creado_fecha_cambio', 'fecha_de_modificacion_cambio', 'eliminado_cambio')	
    list_filter       = ('eliminado_cambio',)
    search_fields     = ('timestamp',)

