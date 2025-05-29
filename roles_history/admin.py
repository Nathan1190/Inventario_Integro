from django.contrib import admin
from .models import Roles_History

@admin.register(Roles_History)
class RolesAdmin(admin.ModelAdmin):
    list_display      = ('rol', 'timestamp', 'nombre_cambio', 'descripcion_cambio', 'eliminado_cambio', 'usuarios_cambio', 'pantallas_cambio', 'fecha_de_creacion_cambio', 'fecha_de_modificacion_cambio')
    list_filter       = ('eliminado_cambio',)
    search_fields     = ('timestamp',)
