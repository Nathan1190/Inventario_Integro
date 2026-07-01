from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

from roles.models import Pantalla, Roles


PANTALLAS = [
    ("0000", "Roles y Permisos"),
    ("0001", "Historial de Roles"),
    ("0002", "Empleados"),
    ("0003", "Historial de Empleados"),
    ("0004", "Cargos"),
    ("0005", "Departamentos"),
    ("0006", "Ubicaciones"),
    ("0007", "Historial de Cargos"),
    ("0008", "Historial de Dependencias"),
    ("0009", "Estados"),
    ("0010", "Proveedores"),
    ("0011", "Historial de Proveedores"),
    ("0012", "Categorías"),
    ("0013", "Historial de Categorías"),
    ("0014", "Bienes Nacionales"),
    ("0015", "Historial de Estados"),
    ("0016", "Sub Categorías"),
    ("0017", "Historial de Sub Categorías"),
    ("0018", "Historial de Inventario"),
    ("0020", "Asignaciones"),
    ("0022", "Historial de Asignaciones"),
    ("0023", "Solicitud de Bienes"),
    ("0024", "Objetos de Gasto"),
    ("0025", "Historial de Objetos de Gasto"),
]


class Command(BaseCommand):
    help = "Crea pantallas, rol Administrador y asigna el superusuario al rol"

    def handle(self, *args, **options):
        User = get_user_model()

        pantallas_creadas = []

        for identificador, nombre in PANTALLAS:
            pantalla, created = Pantalla.objects.get_or_create(
                identificador=identificador,
                defaults={"nombre": nombre}
            )
            pantallas_creadas.append(pantalla)

        admin_role, created = Roles.objects.get_or_create(
            nombre="Administrador",
            defaults={
                "descripcion": "Rol con acceso completo al sistema",
                "eliminado": False,
            }
        )

        admin_role.pantallas.set(pantallas_creadas)
        admin_role.save()

        username = config("DJANGO_SUPERUSER_USERNAME", default="admin")

        superuser = User.objects.filter(username=username, is_superuser=True).first()

        if superuser:
            admin_role.users.add(superuser)
            self.stdout.write(
                self.style.SUCCESS(
                    f"El usuario '{username}' fue asignado al rol Administrador."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"No se encontró el superusuario '{username}'. Primero crea el superusuario."
                )
            )

        self.stdout.write(
            self.style.SUCCESS("Pantallas y rol Administrador configurados correctamente.")
        )