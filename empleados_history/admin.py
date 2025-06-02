from django.contrib import admin
from .models import Empleados_History

@admin.register(Empleados_History)
class RolesAdmin(admin.ModelAdmin):
    list_display      = ('id', 'empleado', 'changed_by', 'timestamp', 'nombre_cambio', 'cargo_cambio', 'dependencia_cambio', 'contacto_cambio', 'correo_inst_cambio', 'codigo_empleado_cambio', 'activo_cambio', 'eliminado_cambio', 'creado_fecha_cambio', 'fecha_de_modificacion_cambio')
    list_filter       = ('eliminado_cambio',)
    search_fields     = ('timestamp',)

