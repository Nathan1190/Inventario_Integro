from django import forms
from .models import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class FormDependencias(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormDependencias, self).__init__(*args, **kwargs)
    

    class Meta:
        model = Dependencias
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. RECURSOS HUMANOS)',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripcion'
            }),
        }

class FormDependenciasDELETE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormDependenciasDELETE, self).__init__(*args, **kwargs)
    

    class Meta:
        model = Dependencias
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo (ej. RECURSOS HUMANOS)',
                'readonly': True,
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripcion',
                'readonly': True,
            }),
            
        }
                
                

