from django import forms
from .models import Empleados
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.validators import RegexValidator

class FormEmpleados(forms.ModelForm):

    class Meta:
        model = Empleados
        fields = [
            'nombre', 'cargo', 'dependencia', 'contacto',
            'correo_inst', 'codigo_empleado', 'activo', 'num_identidad', 'user', 'eliminado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. Mario Luis)'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control select2'
            }),
            'dependencia': forms.Select(attrs={
                'class': 'form-control select2'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+504 1234-5678',
                'type': 'tel',
                'id': 'id_contacto',
            }),
            'correo_inst': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@utpoliticalimpia.hn',
                'pattern': r'^[\w\.\-]+@utpoliticalimpia\.hn$',
                'title': 'Debe terminar en @utpoliticalimpia.hn'
            }),
            'codigo_empleado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '4 dígitos, ej. 7016',
                'pattern': r'^\d{4}$',
                'title': 'Sólo 4 dígitos numéricos'
            }),
            'num_identidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0801-2000-00000',
                'title': 'Sólo 13 dígitos separados por guiones',
            }),

            'user': forms.Select(attrs={
                'class': 'form-control select2',
            }),

            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
            'eliminado': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }

    def clean_correo_inst(self):
        email = self.cleaned_data.get('correo_inst', '').strip().lower()
        # Aunque ya valida el regex, nos aseguramos:
        if not email.endswith('@utpoliticalimpia.hn'):
            raise forms.ValidationError('El correo debe pertenecer al dominio @utpoliticalimpia.hn')
        return email

    def clean_codigo_empleado(self):
        code = self.cleaned_data.get('codigo_empleado', '').strip()
        if not code.isdigit() or len(code) != 4:
            raise forms.ValidationError('El código debe tener exactamente 4 dígitos numéricos.')
        return code
    
    def clean_numero_inventario(self):
        code = self.cleaned_data.get('num_empleado', '').strip()
        #if not code.isdigit() or len(code) != 15:
        #   raise forms.ValidationError('El código debe tener exactamente 4 dígitos numéricos.')
        #return code


class FormEmpleadosDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormEmpleadosDELETE, self).__init__(*args, **kwargs)
        # Hacemos todos los campos de solo lectura
        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs['readonly'] = True
            if field_name in ['activo', 'eliminado']:
                widget.attrs['disabled'] = True

    class Meta:
        model = Empleados
        fields = [
            'nombre', 'cargo', 'dependencia', 'contacto',
            'correo_inst', 'codigo_empleado', 'num_identidad', 'user', 'activo', 'eliminado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. Mario Luis)',
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'dependencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dependencia (ej. Recursos Humanos)',
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234-5678',
            }),
            'correo_inst': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@utpoliticalimpia.hn',
            }),
            'codigo_empleado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '4 dígitos, ej. 1000',
            }),
            'num_identidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0801-2000-00000',
                'title': 'Sólo 13 dígitos separados por guiones',
            }),
            'user': forms.TextInput(attrs={
                'class': 'form-control select2',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
            'eliminado': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }
