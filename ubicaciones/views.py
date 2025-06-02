# ubicaciones/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from roles.mixins import PantallaRequiredMixin
from .models import Ubicaciones
from .forms import FormUbicaciones, FormUbicacionesDELETE

class UbicacionesList(PantallaRequiredMixin, ListView):
    model               = Ubicaciones
    template_name       = 'Ubicaciones/CRUD/index.html'
    context_object_name = "Ubicaciones"
    pantalla_required   = '0006'
    paginate_by         = 20

    def get_queryset(self):
        return Ubicaciones.objects.filter(eliminado=False).order_by('-creado_fecha')


class UbicacionesCreate(PantallaRequiredMixin, CreateView):
    model              = Ubicaciones
    form_class         = FormUbicaciones
    template_name      = 'Ubicaciones/CRUD/add.html'
    success_url        = reverse_lazy('ubicaciones:home_ubicaciones')
    pantalla_required  = '0006'


class UbicacionesEdit(PantallaRequiredMixin, UpdateView):
    model              = Ubicaciones
    form_class         = FormUbicaciones
    template_name      = 'Ubicaciones/CRUD/edit.html'
    success_url        = reverse_lazy('ubicaciones:home_ubicaciones')
    pantalla_required  = '0006'


class UbicacionesDelete(PantallaRequiredMixin, UpdateView):
    model              = Ubicaciones
    form_class         = FormUbicacionesDELETE
    template_name      = 'Ubicaciones/CRUD/delete.html'
    success_url        = reverse_lazy('ubicaciones:home_ubicaciones')
    pantalla_required  = '0006'

    def post(self, request, pk):
        obj = get_object_or_404(Ubicaciones, pk=pk)
        obj.eliminado = True
        obj.save()
        return redirect(self.success_url)
