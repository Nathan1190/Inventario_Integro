from django.contrib import admin
from .models import Empleados

@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    list_display      = ('id', 'nombre', 'cargo', 'dependencia', 'contacto', 'correo_inst', 'codigo_empleado', 'num_identidad', 'user', 'activo', 'eliminado', 'creado_fecha', 'fecha_de_modificacion')
    list_filter       = ('eliminado',)
    search_fields     = ('nombre',)
