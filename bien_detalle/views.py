from django.shortcuts import render
from django.views.generic import ListView
from inventario.models import BienNacional
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from inventario.models import BienNacional
from inventario.forms import BienNacionalEditForm
from django.urls import reverse_lazy

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
    
class BienDetalleEdit(UpdateView):
    
    model = BienNacional
    form_class = BienNacionalEditForm
    template_name = "BienDetalle/edit.html"

    class Meta:
        model = BienNacional
        exclude = [
            'numero_inventario', 'eliminado', 'creado', 'modificado',
            'total_asignado', 'cantidad_restante',  # se actualizan automáticos
        ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'total_bienes' in form.fields:
            del form.fields['total_bienes']
        if 'cantidad_minima' in form.fields:
            form.fields['cantidad_minima'].required = False
        return form

    def get_success_url(self):
        bien = self.object
        return reverse_lazy(
            'bien_detalle:desagrupado',
            kwargs={
                'nombre_bien': bien.nombre_bien,
                'categoria_id': bien.categoria.id,
                'subcategoria_id': bien.subcategoria.id if bien.subcategoria else 0
            }
        )
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Errores del formulario:", form.errors)  # Esto imprime los errores en tu consola de Django
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
