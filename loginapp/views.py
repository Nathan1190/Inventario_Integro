# loginapp/views.py
import re
from django.shortcuts       import render, redirect
from django.contrib         import messages
from django.contrib.auth    import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache  import never_cache
from .forms import *

def validar_email_unico(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('Este correo electrónico ya está en uso.')

@never_cache
@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 1) Crear usuario
            u = User.objects.create_user(
                username   = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name  = form.cleaned_data['last_name'],
                email      = form.cleaned_data['email'],
                password   = form.cleaned_data['password1'],
            )
            # 2) Loguearlo (opcional)
            auth_login(request, u)
            # 3) Mostrar pantalla de éxito
            return render(request, 'loginapp/register_success.html')
    else:
        form = RegistrationForm()

    return render(request, 'loginapp/register.html', {'form': form})


@never_cache
@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        login_input = request.POST['login'].strip()  # quita espacios
        pw          = request.POST['password']

        # Detecta si es email o username
        is_email = '@' in login_input

        if is_email:
            try:
                # búsqueda case-insensitive sobre el email
                user_obj = User.objects.get(email__iexact=login_input)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, 'Usuario o contraseña inválidos.')
                return redirect('loginapp:login')
        else:
            # búsqueda case-insensitive sobre el username
            try:
                user_obj = User.objects.get(username__iexact=login_input)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, 'Usuario o contraseña inválidos.')
                return redirect('loginapp:login')

        # Autentica con el username verdadero
        user = authenticate(request, username=username, password=pw)
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
            return redirect('loginapp:login')

    return render(request, 'loginapp/login.html')


def logout(request):
    auth_logout(request)
    return redirect('loginapp:login')
