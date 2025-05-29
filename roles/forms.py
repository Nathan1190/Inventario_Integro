# roles/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Roles, Pantalla

User = get_user_model()

class FormRoles(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control dual-listbox',
            'size': 8
        }),
        label='Usuarios asignados'
    )
    pantallas = forms.ModelMultipleChoiceField(
        queryset=Pantalla.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control dual-listbox',
            'size': 8
        }),
        label='Pantallas activas'
    )

    class Meta:
        model  = Roles
        fields = ['nombre', 'descripcion', 'eliminado', 'users', 'pantallas']
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'eliminado':   forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'}),
        }

class FormRolesDELETE(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control dual-listbox',
            'size': 8,
            'readonly': True,
            'disabled': True
        }),
        label='Usuarios asignados'
    )
    pantallas = forms.ModelMultipleChoiceField(
        queryset=Pantalla.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control dual-listbox',
            'size': 8,
            'readonly': True,
            'disabled': True
        }),
        label='Pantallas activas'
    )

    class Meta:
        model  = Roles
        fields = ['nombre', 'descripcion', 'eliminado', 'users', 'pantallas']
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'disabled': True}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'disabled': True}),
            'eliminado':   forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'}),
        }
