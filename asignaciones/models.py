from django.db import models
from inventario.models import BienNacional
from empleados.models import Empleados
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.middleware import get_current_user

ESTADOS_ASIGNACION = [
    ('pendiente', 'Pendiente de firma'),
    ('firmado', 'Firmado/Entregado'),
    ('cancelado', 'Cancelado'),
]

class AsignacionBien(models.Model):
    bien = models.ForeignKey(BienNacional, on_delete=models.CASCADE, related_name='asignaciones')
    responsable = models.ForeignKey(Empleados, on_delete=models.CASCADE, related_name='asignaciones_recibidas')
    asignado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones_realizadas')
    estado = models.CharField(max_length=20, choices=ESTADOS_ASIGNACION, default='pendiente')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_firma = models.DateTimeField(null=True, blank=True)
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
        fecha_firma=instance.fecha_firma,
        comentario=instance.comentario,
        changed_by= user,  
        cambiado_en=instance.updated_at if hasattr(instance, "updated_at") else instance.fecha_asignacion,
    )