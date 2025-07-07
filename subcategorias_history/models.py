from django.db import models
from subcategorias.models import Subcategorias
from django.conf import settings

class Subcategorias_History(models.Model):
    subcategoria = models.ForeignKey(
        Subcategorias,
        on_delete=models.CASCADE,
        related_name="historial"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Modificado por"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    # Campos “snapshot” de Subcategoría
    nombre_cambio                = models.CharField(max_length=80)
    descripcion_cambio           = models.CharField(max_length=120, blank=True)
    categoria_cambio             = models.CharField(max_length=80)
    creado_fecha_cambio          = models.DateTimeField()
    fecha_de_modificacion_cambio = models.DateTimeField()
    eliminado_cambio             = models.BooleanField()

    class Meta:
        ordering  = ["-timestamp"]
        verbose_name_plural = "Historial de subcategorías"

    def __str__(self):
        user = self.changed_by.username if self.changed_by else "Sistema"
        return f"Hist/Subcat {self.subcategoria} por {user} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
