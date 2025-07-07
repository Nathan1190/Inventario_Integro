from django.db import models
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator,
    EmailValidator
)
from cargos.models import Cargos 
from dependencias.models import Dependencias  
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.middleware import get_current_user
from django.contrib.auth.models import User


class Empleados(models.Model):
    # ─── Validadores comunes ───
    regex_letras_espacios = RegexValidator(
        regex=r'^[A-Za-z\s]+$',
        message='Sólo letras y espacios. Después se convertirá todo a mayúsculas.'
    )
    # Nombre/cargo/dependencia: entre 2 y 80 caracteres
    min2 = MinLengthValidator(2, 'Mínimo 2 caracteres.')
    max80 = MaxLengthValidator(80, 'Máximo 80 caracteres.')

    # Contacto: dígitos, espacios, + y - (e.g. "+504 1234-5678")
    regex_contacto = RegexValidator(
        regex=r'^[0-9+\-\s]+$',
        message='Contacto sólo puede tener dígitos, espacios, + y -.'
    )
    max120 = MaxLengthValidator(120, 'Máximo 120 caracteres.')

    # Correo institucional: sólo dominio @utpoliticalimpia.hn
    regex_email_inst = RegexValidator(
        regex=r'^[\w\.\-]+@utpoliticalimpia\.hn$',
        message='Debes usar tu correo institucional terminando en @utpoliticalimpia.hn'
    )

    # Código de empleado: sólo dígitos, 4 caracteres (ajustable)
    regex_codigo = RegexValidator(
        regex=r'^\d{4}$',
        message='El código de empleado debe tener exactamente 4 dígitos, p.ej. "7016".'
    )

    # ─── Campos ───
    nombre = models.CharField(
        max_length=120,
        validators=[regex_letras_espacios, MinLengthValidator(2), MaxLengthValidator(120)]
    )
    cargo = models.ForeignKey(
        Cargos,
        on_delete=models.PROTECT,
    )
    dependencia = models.ForeignKey(
        Dependencias,
        on_delete=models.PROTECT,
    )
    contacto = models.CharField(
        max_length=120,
        validators=[regex_contacto, max120]
    )

    correo_inst = models.CharField(
        "Correo institucional",
        max_length=100,
        unique=True,
        validators=[regex_email_inst, EmailValidator(message='Formato de correo inválido.')],
        help_text='Debe terminar en @utpoliticalimpia.hn'
    )
    codigo_empleado = models.CharField(
        "Código de empleado",
        max_length=4,
        unique=True,
        validators=[regex_codigo],
        help_text='Exactamente 4 dígitos, p.ej. 7016',
    )

    num_identidad = models.CharField(
        "Numero de Identidad",
        max_length=15,
        unique=True,
        help_text='Debe contener 13 digitos en total, separados por guiones p.ej. 0801-2000-00000',
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        related_name='empleados'
    )

    activo = models.BooleanField(default=False)
    creado_fecha = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.codigo_empleado} - {self.nombre} - {self.num_identidad}"

    def clean(self):
        super_clean = super().clean() if hasattr(super(), 'clean') else None

        for field in ['nombre']:
            val = getattr(self, field, '')
            if isinstance(val, str):
                setattr(self, field, val.strip().upper())

        if isinstance(self.correo_inst, str):
            self.correo_inst = self.correo_inst.strip().lower()

        if isinstance(self.codigo_empleado, str):
            self.codigo_empleado = self.codigo_empleado.strip()

        if isinstance(self.contacto, str):
            self.contacto = self.contacto.strip()

        return super_clean

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=Empleados)
def create_empleado_history(sender, instance, created, **kwargs):
    from empleados_history.models import Empleados_History
    usuario = get_current_user()  
    Empleados_History.objects.create(
        empleado                     = instance,
        changed_by                   = usuario,
        nombre_cambio                = instance.nombre,
        cargo_cambio                 = str(instance.cargo),
        dependencia_cambio           = str(instance.dependencia),
        contacto_cambio              = instance.contacto,
        correo_inst_cambio           = instance.correo_inst,
        codigo_empleado_cambio       = instance.codigo_empleado,
        numero_identidad_cambio      = instance.num_identidad,
        user_cambio                  = instance.user.username if instance.user else "",
        activo_cambio                = instance.activo,
        creado_fecha_cambio          = instance.creado_fecha,
        fecha_de_modificacion_cambio = instance.fecha_de_modificacion,
        eliminado_cambio             = instance.eliminado
    )

