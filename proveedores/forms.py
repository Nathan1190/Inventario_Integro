from django import forms
from .models import Proveedores
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.validators import RegexValidator

class FormProveedores(forms.ModelForm):

    class Meta:
        model = Proveedores
        fields = [
            'nombre', 'descripcion', 'telefono', 'correo',
            'direccion', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. PLASTILLOS S.A.)',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234-5678',
                'type': 'tel',
                'id': 'id_telefono',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@dominio.com',
                'pattern': r'^[\w\.\+\-]+@[\w\-]+\.[A-Za-z]{2,}$',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la direccion del proveedor (ej. Lomas del Mayab, Tegucigalpa, ...)',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }

    def clean_correo_inst(self):
        email = self.cleaned_data.get('correo_inst', '').strip().lower()
        return email

class FormProveedoresDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormProveedoresDELETE, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs['readonly'] = True
            if field_name in ['activo', 'eliminado']:
                widget.attrs['disabled'] = True

    class Meta:
        model = Proveedores
        fields = [
            'nombre', 'descripcion', 'telefono', 'correo',
            'direccion', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. PLASTILLOS S.A.)',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234-5678',
                'type': 'tel',
                'id': 'id_telefono',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@dominio.com',
                'pattern': r'^[\w\.\+\-]+@[\w\-]+\.[A-Za-z]{2,}$',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la direccion del proveedor (ej. Lomas del Mayab, Tegucigalpa, ...)',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }
