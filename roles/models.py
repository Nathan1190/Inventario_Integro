# roles/models.py
from django.db import models
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator
)
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core.middleware import get_current_user


User = get_user_model()

# ─── Validadores para el modelo Pantalla ───

# Nombre: solo letras, espacios, acentos y mínimo 3 caracteres
nombre_pantalla_regex = [
    (r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', 
     'El nombre solo permite letras y espacios.')
]
validators_nombre_pantalla = [
    RegexValidator(regex=pat, message=msg)
    for pat, msg in nombre_pantalla_regex
]
validators_nombre_pantalla += [MinLengthValidator(3)]

# Identificador: solo minúsculas, números, guiones bajos y barras
ident_regex = [
    (r'^[a-z0-9_/:-]+$',
     'El identificador solo permite minúsculas, números, guiones bajos, "/" o ":"')
]
validators_identificador = [
    RegexValidator(regex=pat, message=msg)
    for pat, msg in ident_regex
]

# ─── Validadores para el modelo Roles ───

# Nombre de rol: letras, espacios y mínimo 3 caracteres, máximo 50
rol_nombre_regex = [
    (r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
     'El nombre solo permite letras y espacios.')
]
validators_nombre_rol = [
    RegexValidator(regex=pat, message=msg)
    for pat, msg in rol_nombre_regex
]
validators_nombre_rol += [MinLengthValidator(3), MaxLengthValidator(50)]

# Descripción: letras, números, espacios y puntuación básica
desc_regex = [
    (r'^[\wÁÉÍÓÚáéíóúÑñ\s\.,;:¡!¿?\"\'\-\(\)]+$',
     'La descripción no permite caracteres extraños.')
]
validators_descripcion = [
    RegexValidator(regex=pat, message=msg)
    for pat, msg in desc_regex
]
validators_descripcion += [MinLengthValidator(5), MaxLengthValidator(160)]



class Pantalla(models.Model):
    nombre = models.CharField(
        'Nombre de la pantalla',
        max_length=100,
        unique=True,
        validators=validators_nombre_pantalla
    )
    identificador = models.CharField(
        'Ruta/ID',
        max_length=100,
        unique=True,
        validators=validators_identificador
    )

    def __str__(self):
        return self.nombre


class Roles(models.Model):
    nombre = models.CharField(
        max_length=50,
        validators=validators_nombre_rol
    )
    descripcion = models.CharField(
        max_length=160,
        validators=validators_descripcion
    )
    eliminado = models.BooleanField(default=False)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='Usuarios asignados',
        related_name='roles'
    )

    pantallas = models.ManyToManyField(
        Pantalla,
        blank=True,
        verbose_name='Pantallas activas',
        related_name='roles'
    )

    def __str__(self):
        return self.nombre

@receiver(post_save, sender=Roles)
def create_roles_history(sender, instance, created, **kwargs):
    from roles_history.models import Roles_History
    user = get_user_model()
    usuarios = ",".join(u.username for u in instance.users.all())
    pantallas= ",".join(p.identificador for p in instance.pantallas.all())

    Roles_History.objects.create(
        rol                        = instance,
        changed_by                 = user,
        nombre_cambio              = instance.nombre,
        descripcion_cambio         = instance.descripcion,
        eliminado_cambio           = instance.eliminado,
        usuarios_cambio            = usuarios,
        pantallas_cambio           = pantallas,
        fecha_de_creacion_cambio   = instance.fecha_de_creacion,
        fecha_de_modificacion_cambio= instance.fecha_de_modificacion,
    )