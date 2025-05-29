from django.contrib import admin
from .models import Roles, Pantalla

@admin.register(Pantalla)
class PantallaAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre', 'identificador')
    search_fields = ('nombre', 'identificador')

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display      = ('id', 'nombre', 'descripcion', 'eliminado', 'fecha_de_creacion', 'fecha_de_modificacion')
    list_filter       = ('eliminado',)
    search_fields     = ('nombre',)
    filter_horizontal = ('pantallas',)
