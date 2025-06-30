from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from roles.mixins import PantallaRequiredMixin
from .models import AsignacionBien
from .forms import AsignacionBienForm
from inventario.models import BienNacional
from django.contrib import messages

class AsignacionBienListView(PantallaRequiredMixin, ListView):
    template_name = 'Asignaciones/lista.html'
    model = AsignacionBien
    context_object_name = 'asignaciones'
    pantalla_required = '0020'  # Define tu código de permiso

    def get_queryset(self):
        return AsignacionBien.objects.select_related('bien', 'responsable').order_by('-fecha_asignacion')

class AsignarBienCreateView(PantallaRequiredMixin, CreateView):
    template_name = 'Asignaciones/asignar.html'
    model = AsignacionBien
    form_class = AsignacionBienForm
    pantalla_required = '0020'

    def dispatch(self, request, *args, **kwargs):
        self.bien = get_object_or_404(BienNacional, pk=kwargs['bien_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['bien'] = self.bien
        # Buscar asignación pendiente
        asignacion_pendiente = AsignacionBien.objects.filter(
            bien=self.bien, estado='pendiente'
        ).first()
        ctx['asignacion_pendiente'] = asignacion_pendiente
        return ctx

    def form_valid(self, form):
        form.instance.bien = self.bien
        form.instance.asignado_por = self.request.user
        form.instance.estado = 'pendiente'
        sobrescribir = self.request.POST.get('sobrescribir', '') == '1'
        
        # Busca si ya hay pendiente para ese bien
        asignacion_existente = AsignacionBien.objects.filter(
            bien=self.bien, estado='pendiente'
        ).first()

        if asignacion_existente and not sobrescribir:
            # Hay pendiente y no está confirmado el reemplazo
            messages.warning(self.request,
                f'Ya existe una asignación pendiente para este bien: '
                f'{asignacion_existente.responsable}. ¿Quieres sobrescribirla?'
            )
            # Recarga el form, pero ahora con 'sobrescribir'
            ctx = self.get_context_data(form=form)
            ctx['show_confirm'] = True
            return self.render_to_response(ctx)
        
        # Si sobrescribir, cancelar la anterior
        if asignacion_existente and sobrescribir:
            asignacion_existente.estado = 'cancelado'
            asignacion_existente.save()
            messages.info(self.request, f'La asignación previa fue cancelada y se creó una nueva.')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bien_detalle:desagrupado', kwargs={
            'nombre_bien': self.bien.nombre_bien,
            'categoria_id': self.bien.categoria.id,
            'subcategoria_id': self.bien.subcategoria.id if self.bien.subcategoria else 0,
        })  

class ConfirmarFirmaView(PantallaRequiredMixin, UpdateView):
    model = AsignacionBien
    fields = []
    template_name = 'Asignaciones/confirmar_firma.html'
    pantalla_required = '0021'  # Otro código de permiso

    def get_object(self, queryset=None):
        return get_object_or_404(AsignacionBien, pk=self.kwargs['pk'], estado='pendiente')

    def post(self, request, *args, **kwargs):
        asignacion = self.get_object()
        asignacion.estado = 'firmado'
        asignacion.fecha_firma = timezone.now()
        asignacion.save()
        # Actualiza el responsable del bien
        bien = asignacion.bien
        bien.responsable = asignacion.responsable
        bien.save()
        # Aquí puedes llamar a crear historial también
        return redirect('bien_detalle:desagrupado',
                        nombre_bien=bien.nombre_bien,
                        categoria_id=bien.categoria.id,
                        subcategoria_id=bien.subcategoria.id if bien.subcategoria else 0)

class CancelarAsignacionView(PantallaRequiredMixin, UpdateView):
    model = AsignacionBien
    fields = []
    template_name = 'asignaciones/cancelar.html'
    pantalla_required = '0021'

    def get_object(self, queryset=None):
        return get_object_or_404(AsignacionBien, pk=self.kwargs['pk'], estado='pendiente')

    def post(self, request, *args, **kwargs):
        asignacion = self.get_object()
        asignacion.estado = 'cancelado'
        asignacion.save()
        # Aquí igual puedes llamar a crear historial
        return redirect('bien_detalle:desagrupado',
                        nombre_bien=asignacion.bien.nombre_bien,
                        categoria_id=asignacion.bien.categoria.id,
                        subcategoria_id=asignacion.bien.subcategoria.id if asignacion.bien.subcategoria else 0)
