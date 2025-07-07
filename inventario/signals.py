from django.db.models.signals import post_save
from django.dispatch import receiver
from core.middleware import get_current_user
from inventario.models import BienNacional
from inventario_history.models import BienNacionalHistory

@receiver(post_save, sender=BienNacional)
def crear_historial_bien(sender, instance, created, **kwargs):
    user = get_current_user()
    BienNacionalHistory.objects.create(
        bien=instance,
        changed_by=user,
        # compania=instance.compania.nombre if instance.compania else '',  # Solo si tienes el campo en el modelo
        nombre_bien=instance.nombre_bien,
        objeto_gasto=instance.objeto_gasto.nombre if instance.objeto_gasto else '',
        categoria=instance.categoria.nombre if instance.categoria else '',
        subcategoria=instance.subcategoria.nombre if instance.subcategoria else '',
        numero_modelo=instance.numero_modelo,
        manufacturera=instance.manufacturera.nombre if instance.manufacturera else '',
        fabricante=instance.fabricante.nombre if instance.fabricante else '',
        proveedor=instance.proveedor.nombre if instance.proveedor else '',
        serial=instance.serial,
        numero_inventario=instance.numero_inventario,
        unidad_medida=instance.unidad_medida,
        ubicacion=instance.ubicacion.nombre if instance.ubicacion else '',
        fecha_compra=instance.fecha_compra,
        costo_compra=instance.costo_compra,
        numero_orden=instance.numero_orden,
        numero_factura=instance.numero_factura,
        estado_fisico=', '.join([e.nombre for e in instance.estado_fisico.all()]) if instance.estado_fisico.exists() else '',
        responsable=instance.responsable if instance.responsable else '',
        notas=instance.notas,
        eliminado=instance.eliminado
    )

