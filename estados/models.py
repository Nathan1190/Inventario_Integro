from django.db import models
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from core.middleware import get_current_user   

_hex_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="Color HEX inválido, ej. #34A853"
)

class Estados(models.Model):
    nombre      = models.CharField("Nombre", max_length=60, unique=True)
    color_hex   = models.CharField(
        "Color (HEX)",
        max_length=7,
        validators=[_hex_validator],
        null=True, blank=True,
        help_text="Opcional. Si se omite, se mostrará un gris neutro."
    )
    descripcion = models.CharField(max_length=120)
    eliminado   = models.BooleanField(default=False)
    creado_en   = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = "estados"
        ordering  = ["nombre"]

    def __str__(self):
        return self.nombre
    
@receiver(post_save, sender=Estados)
def create_estado_history(sender, instance, created, **kwargs):
    from estados_history.models import Estados_History
    user = get_current_user()  
    Estados_History.objects.create(
        estado                       = instance,
        changed_by                   = user,
        nombre_cambio                = instance.nombre,
        color_hex_cambio             = instance.color_hex,
        descripcion_cambio           = instance.descripcion,
        creado_en_cambio             = instance.creado_en,
        actualizado_en_cambio        = instance.actualizado_en,
        eliminado_cambio             = instance.eliminado
    )





