from django.db import models
from inventario.models import BienNacional
from empleados.models import Empleados
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.middleware import get_current_user

import os
import datetime
from uuid import uuid4

ESTADOS_ASIGNACION = [
    ('pendiente', 'Pendiente'),
    ('proceso', 'Proceso'),
    ('firmado', 'Firmado'),
    ('cancelado', 'Cancelado'),
    ('penddesc', 'PendDesc'),
    ('descargado', 'Descargado'),
]

def firma_documento_upload_path(instance, filename):
    # Usa el número de inventario si existe, si no un uuid
    today = str(datetime.date.today())
    ext = filename.split('.')[-1]
    
    
    # Decide la carpeta según estado
    if instance.estado in ['descargado', 'penddesc']:
        nombre = today + " - " + str(uuid4()) + "DESCARGO"
        carpeta = "descargos"
    else:
        nombre = today + " - " + str(uuid4()) + "CARGOS"
        carpeta = "cargos"
    filename = f"{nombre}.{ext}"
    return os.path.join("assets", "asignaciones", carpeta, filename)

class AsignacionBien(models.Model):
    bien = models.ForeignKey(BienNacional, on_delete=models.CASCADE, related_name='asignaciones')
    responsable = models.ForeignKey(Empleados, on_delete=models.CASCADE, related_name='asignaciones_recibidas')
    asignado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones_realizadas')
    estado = models.CharField(max_length=20, choices=ESTADOS_ASIGNACION, default='pendiente')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_aceptado = models.DateTimeField(null=True, blank=True)
    fecha_firma = models.DateTimeField(null=True, blank=True)
    fecha_descargo = models.DateTimeField(null=True, blank=True)
    pdf_firmado = models.FileField(upload_to=firma_documento_upload_path, null=True, blank=True, verbose_name="PDF Firmado")
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.bien} -> {self.responsable} ({self.get_estado_display()})"
    
@receiver(post_save, sender=AsignacionBien)
def crear_historial_asignacion(sender, instance, created, **kwargs):
    """
    Crea un historial cada vez que una asignación se crea o cambia de estado.
    """
    from asignaciones.models import AsignacionBien
    from asignaciones_history.models import Asignaciones_History
    user = get_current_user()
    
    Asignaciones_History.objects.create(
        asignacion=instance,
        bien=instance.bien,
        responsable=instance.responsable,
        estado=instance.estado,
        asignado_por=instance.asignado_por,
        fecha_asignacion=instance.fecha_asignacion,
        fecha_aceptado=instance.fecha_aceptado,
        fecha_firma=instance.fecha_firma,
        fecha_descargo=instance.fecha_descargo,
        pdf_firmado=instance.pdf_firmado,
        comentario=instance.comentario,
        changed_by= user,  
        cambiado_en=instance.updated_at if hasattr(instance, "updated_at") else instance.fecha_asignacion,
    )