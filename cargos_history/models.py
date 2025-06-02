# cargos_history/models.py

from django.db import models
from django.conf import settings
from cargos.models import Cargos

class Cargos_History(models.Model):
    cargo = models.ForeignKey(
        Cargos,
        on_delete=models.CASCADE,
        related_name='historial'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Modificado por"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    nombre_cambio                 = models.CharField(max_length=120)
    descripcion_cambio            = models.CharField(max_length=120)
    eliminado_cambio              = models.BooleanField()
    creado_fecha_cambio           = models.DateTimeField()
    fecha_de_modificacion_cambio  = models.DateTimeField()

    class Meta:
        db_table = "cargos_history"
        ordering = ["-timestamp"]

    def __str__(self):
        user = self.changed_by.username if self.changed_by else "Desconocido"
        return f"Historial de {self.cargo.nombre} por {user} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
