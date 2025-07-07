
from django import forms
from inventario.models import BienNacional

class BienNacionalDeleteForm(forms.ModelForm):
    """
    Form solo-lectura para confirmación de borrado (soft-delete).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["readonly"] = True
            field.widget.attrs["disabled"] = True

    class Meta:
        model = BienNacional
        fields = [
            'numero_inventario', 'nombre_bien', 'objeto_gasto', 'categoria', 'subcategoria',
            'compania', 'manufacturera', 'fabricante', 'proveedor',
            'serial', 'unidad_medida', 'ubicacion', 'fecha_compra',
            'costo_compra', 'numero_orden', 'numero_factura', 'notas',
            'responsable'
        ]