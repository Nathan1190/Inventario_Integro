from django import forms
from .models import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class FormCargos(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormCargos, self).__init__(*args, **kwargs)
    

    class Meta:
        model = Cargos
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. GERENTE DE LOGISTICA)'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripcion'
            }),
        }

class FormCargosDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormCargosDELETE, self).__init__(*args, **kwargs)
    

    class Meta:
        model = Cargos
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. GERENTE DE LOGISTICA)',
                'readonly': True,
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripcion',
                'readonly': True,
            }),
            
        }
                
                

