from django.contrib import admin
from .models import Subcategorias

@admin.register(Subcategorias)
class SubcategoriasAdmin(admin.ModelAdmin):
    list_display   = (
        "id",
        "nombre",
        "descripcion",
        "categoria",
        "eliminado",
        "creado_fecha",
        "fecha_de_modificacion",
    )
    list_filter    = ("eliminado", "creado_fecha", "fecha_de_modificacion", "categoria")
    search_fields  = ("nombre", "descripcion", "categoria__nombre")
    ordering       = ("id",)
    date_hierarchy = "creado_fecha"
    readonly_fields = ("creado_fecha", "fecha_de_modificacion")
