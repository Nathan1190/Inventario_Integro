# ubicaciones/forms.py

from django import forms
from .models import Ubicaciones

class FormUbicaciones(forms.ModelForm):
    class Meta:
        model = Ubicaciones
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre (ej. PLANTA ALTA)',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'activo': 'Activo',
        }


class FormUbicacionesDELETE(forms.ModelForm):
    """
    Formulario solo lectura para confirmar eliminación (marcar `eliminado=True`).
    """
    def __init__(self, *args, **kwargs):
        super(FormUbicacionesDELETE, self).__init__(*args, **kwargs)
        # deshabilitar todos los campos
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['readonly'] = True
            self.fields[field_name].widget.attrs['disabled'] = True

    class Meta:
        model = Ubicaciones
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'activo': 'Activo',
        }
