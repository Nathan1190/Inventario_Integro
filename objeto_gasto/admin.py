from django.contrib import admin
from .models import ObjetoGasto

@admin.register(ObjetoGasto)
class ObjetoGastoAdmin(admin.ModelAdmin):
    list_display   = (
        "id",
        "nombre",
        "descripcion",
        "eliminado",
        "creado_fecha",
        "fecha_de_modificacion",
    )
    list_filter    = ("eliminado", "creado_fecha", "fecha_de_modificacion")
    search_fields  = ("nombre", "descripcion")
    ordering       = ("id",)
    date_hierarchy = "creado_fecha"
    readonly_fields = ("creado_fecha", "fecha_de_modificacion")
