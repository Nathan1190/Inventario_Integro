from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from roles.mixins import PantallaRequiredMixin
from .models import SolicitudBien
from .forms import SolicitudBienForm

class SolicitudBienCreateView(PantallaRequiredMixin, CreateView):
    model = SolicitudBien
    form_class = SolicitudBienForm
    template_name = 'Solicitud/solicitud_form.html'
    success_url = reverse_lazy('solicitud:listar')
    pantalla_required = '0023'

    def form_valid(self, form):
        empleado = self.request.user.empleados 
        form.instance.solicitante = empleado
        form.instance.dependencia = empleado.dependencia
        response = super().form_valid(form)
        return response

class SolicitudBienListView(PantallaRequiredMixin, ListView):
    model = SolicitudBien
    template_name = 'Solicitud/solicitud_list.html'
    context_object_name = 'solicitudes'
    pantalla_required = '0023'

    def get_queryset(self):
        empleado = self.request.user.empleados
        # Si es admin puedes mostrar todas, si no solo las suyas:
        return SolicitudBien.objects.filter(solicitante=empleado)

class SolicitudBienDetailView(PantallaRequiredMixin, DetailView):
    model = SolicitudBien
    template_name = 'Solicitud/solicitud_detail.html'
    context_object_name = 'solicitud'
    pantalla_required = '0023'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
