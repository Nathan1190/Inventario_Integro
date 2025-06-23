from django.shortcuts import render
from django.views.generic import ListView
from inventario.models import BienNacional

class BienDetalleList(ListView):
    template_name = "BienDetalle/desagrupado.html"
    context_object_name = "bienes"

    def get_queryset(self):
        
        nombre_bien = self.kwargs['nombre_bien']
        categoria_id = self.kwargs['categoria_id']
        subcategoria_id = self.kwargs['subcategoria_id']
        return BienNacional.objects.filter(
            eliminado=False,
            nombre_bien=nombre_bien,
            categoria_id=categoria_id,
            subcategoria_id=subcategoria_id
        ).order_by('id')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['nombre_bien'] = self.kwargs['nombre_bien']
        ctx['categoria_id'] = self.kwargs['categoria_id']
        ctx['subcategoria_id'] = self.kwargs['subcategoria_id']

        # Lógica de imagen heredada
        bienes = list(ctx['bienes'])  # Es el queryset
        # Busca la primera imagen disponible en el grupo
        bien_con_imagen = None
        for bien in bienes:
            if bien.imagen:
                bien_con_imagen = bien
                break
        imagen_grupo = bien_con_imagen.imagen.url if bien_con_imagen and bien_con_imagen.imagen else None

        # Asigna imagen_mostrar a cada bien
        for bien in bienes:
            bien.imagen_mostrar = bien.imagen.url if bien.imagen else imagen_grupo

        # AHORA ACTUALIZA EL CONTEXTO CON LA LISTA
        ctx['bienes'] = bienes

        return ctx 
