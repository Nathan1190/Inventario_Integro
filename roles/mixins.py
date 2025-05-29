# roles/mixins.py
from django.contrib import messages
from django.shortcuts  import redirect

class PantallaRequiredMixin:
    """
    Mixin para CBV que comprueba que el usuario tenga
    activa la pantalla cuya identificador coincida con
    `self.pantalla_required`.
    """
    pantalla_required: str = ''  # debe declararse en la CBV

    def dispatch(self, request, *args, **kwargs):
        # 1) Usuario autenticado
        if not request.user.is_authenticated:
            return redirect('loginapp:login')

        # 2) Lista de identificadores de pantallas activas
        pantallas = request.user.roles.values_list(
            'pantallas__identificador', flat=True
        )

        # 3) Comprobación
        if self.pantalla_required not in pantallas:
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('home')

        # 4) Si todo ok, continúa con la vista normal
        return super().dispatch(request, *args, **kwargs)
