from django import forms
from .models import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class FormEmpleados(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormEmpleados, self).__init__(*args, **kwargs)
    

    class Meta:
        model = Empleados
        fields = ['nombre', 'cargo', 'dependencia', 'contacto', 'activo', 'eliminado']
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
                'id':   'id_contacto',    
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
            'eliminado': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }

class FormEmpleadosDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormEmpleadosDELETE, self).__init__(*args, **kwargs)
    

    class Meta:
        model = Empleados
        fields = ['nombre', 'cargo', 'dependencia', 'contacto', 'activo', 'eliminado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. Mario Luis)',
                'readonly': True,
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'dependencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dependencia (ej. Recursos Humanos)',
                'readonly': True,
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese datos de contacto (ej. +504 1234-5678)',
                'readonly': True,
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
                'readonly': True,
                'disabled': True,
            }),
            'eliminado': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
            }),
        }
                
                

