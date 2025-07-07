from django.db import models

from categorias.models import Categorias
from django.conf import settings


class Categorias_History(models.Model):
    categoria = models.ForeignKey(
        Categorias,
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

    # Campos “snapshot” de Categorías
    nombre_cambio                = models.CharField(max_length=80)
    descripcion_cambio           = models.CharField(max_length=120, blank=True)
    objeto_gasto_cambio          = models.CharField(max_length=120)
    creado_fecha_cambio          = models.DateTimeField()
    fecha_de_modificacion_cambio = models.DateTimeField()
    eliminado_cambio             = models.BooleanField()

    class Meta:
        db_table  = "categorias_history"
        ordering  = ["-timestamp"]
        verbose_name_plural = "Historial de categorías"

    def __str__(self):
        user = self.changed_by.username if self.changed_by else "Sistema"
        return f"Hist/Cat {self.categoria} por {user} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"



