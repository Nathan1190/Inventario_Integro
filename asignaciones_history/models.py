# asignaciones_history/models.py
from django.db import models
from asignaciones.models import AsignacionBien
from django.contrib.auth.models import User
from asignaciones.models import AsignacionBien
from inventario.models import BienNacional
from empleados.models import Empleados
from django.contrib.auth import get_user_model

class Asignaciones_History(models.Model):
    asignacion = models.ForeignKey(AsignacionBien, on_delete=models.CASCADE)
    bien = models.ForeignKey(BienNacional, on_delete=models.SET_NULL, null=True)
    responsable = models.ForeignKey(Empleados, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20)
    asignado_por = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='asignaciones_hechas')
    fecha_asignacion = models.DateTimeField()
    fecha_aceptado = models.DateTimeField(null=True, blank=True)
    fecha_firma = models.DateTimeField(null=True, blank=True)
    fecha_descargo = models.DateTimeField(null=True, blank=True)
    pdf_firmado = models.FileField(null=True,blank=True,upload_to='assets/asignaciones/firmados/',verbose_name="PDF Firmado")
    comentario = models.TextField(null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='asignacion_cambios')
    cambiado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Historial {self.asignacion_id} - {self.estado}'

