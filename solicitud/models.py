from django.db import models
from empleados.models import Empleados
from dependencias.models import Dependencias
from inventario.models import BienNacional
from categorias.models import Categorias
from subcategorias.models import Subcategorias
from objeto_gasto.models import ObjetoGasto
from uuid import uuid4
import os
import datetime

# Puedes adaptar o mover a un archivo separado de enums/catálogo si prefieres.
PRIORIDAD_CHOICES = [
    ('baja', 'Baja'),
    ('media', 'Media'),
    ('alta', 'Alta'),
]

ESTADO_SOLICITUD_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aprobada', 'Aprobada'),
    ('rechazada', 'Rechazada'),
    ('en_proceso', 'En proceso'),
    ('finalizada', 'Finalizada'),
]

def bien_memo_upload_path(instance, filename):
    # Usa el número de inventario si existe, si no un uuid
    today = str(datetime.date.today())
    ext = filename.split('.')[-1]
    nombre = today + " - " + str(uuid4())
    filename = f"{nombre}.{ext}"
    # Retorna la ruta relativa desde MEDIA_ROOT
    return os.path.join("assets", "solicitudes", "memo", filename)


class SolicitudBien(models.Model):
    solicitante = models.ForeignKey(Empleados, on_delete=models.PROTECT, related_name='solicitudes_realizadas')
    memo = models.FileField(upload_to=bien_memo_upload_path, null=True, blank=True, verbose_name='Memo de Solicitud')
    dependencia = models.ForeignKey(Dependencias, on_delete=models.PROTECT)
    objeto_gasto = models.ForeignKey(ObjetoGasto, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categorias, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategorias, on_delete=models.PROTECT)
    bien = models.ForeignKey(BienNacional, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    comentario = models.TextField(verbose_name="Motivo/Comentario", blank=False)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    estado = models.CharField(max_length=15, choices=ESTADO_SOLICITUD_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Solicitudes de Bienes"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Solicitud #{self.id} - {self.solicitante} - {self.bien} ({self.estado})"
