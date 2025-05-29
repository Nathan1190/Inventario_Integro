# loginapp/forms.py

import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label="Nombre",
        min_length=2,
        max_length=30,
        error_messages={
            'required': 'El nombre es obligatorio.',
            'min_length': 'El nombre debe tener al menos 2 caracteres.',
            'max_length': 'El nombre no puede exceder 30 caracteres.'
        },
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Nombre'
        })
    )
    last_name = forms.CharField(
        label="Apellido",
        min_length=2,
        max_length=30,
        error_messages={
            'required': 'El apellido es obligatorio.',
            'min_length': 'El apellido debe tener al menos 2 caracteres.',
            'max_length': 'El apellido no puede exceder 30 caracteres.'
        },
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Apellido'
        })
    )
    username = forms.CharField(
        label="Usuario",
        min_length=4,
        max_length=30,
        error_messages={
            'required': 'El usuario es obligatorio.',
            'min_length': 'El usuario debe tener al menos 4 caracteres.',
            'max_length': 'El usuario no puede exceder 30 caracteres.'
        },
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Usuario'
        })
    )
    email = forms.EmailField(
        label="E-mail",
        error_messages={
            'required': 'El correo es obligatorio.',
            'invalid': 'Ingrese un correo electrónico válido.'
        },
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'E-mail'
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        min_length=8,
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'min_length': 'La contraseña debe tener al menos 8 caracteres.'
        },
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Contraseña'
        })
    )
    password2 = forms.CharField(
        label="Repite contraseña",
        error_messages={
            'required': 'Debes confirmar la contraseña.'
        },
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Repite contraseña'
        })
    )

    def clean_first_name(self):
        fn = self.cleaned_data['first_name'].strip()
        if not fn.isalpha():
            raise ValidationError("El nombre solo puede contener letras.")
        return fn.upper()

    def clean_last_name(self):
        ln = self.cleaned_data['last_name'].strip()
        if not ln.isalpha():
            raise ValidationError("El apellido solo puede contener letras.")
        return ln.upper()

    def clean_username(self):
        un = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=un).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]+$', un):
            raise ValidationError("El usuario solo puede contener letras, números o guión bajo, y no iniciar con número.")
        return un

    def clean_email(self):
        em = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=em).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        return em

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("password1")
        pw2 = cleaned.get("password2")

        # Validar coincidencia
        if pw1 and pw2:
            if pw1 != pw2:
                raise ValidationError("Las contraseñas no coinciden.")

            # Validaciones de complejidad
            if len(pw1) < 8:
                raise ValidationError("La contraseña debe tener mínimo 8 caracteres.")
            if not re.search(r'[A-Z]', pw1):
                raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
            if not re.search(r'[a-z]', pw1):
                raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
            if not re.search(r'\d', pw1):
                raise ValidationError("La contraseña debe contener al menos un dígito.")
            if not re.search(r'[^A-Za-z0-9]', pw1):
                raise ValidationError("La contraseña debe contener al menos un carácter especial.")

        return cleaned
