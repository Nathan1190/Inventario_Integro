from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import Estados
from roles.mixins import PantallaRequiredMixin

class EstadosList(PantallaRequiredMixin, ListView):
    template_name        = 'Estados/CRUD/index.html'
    queryset             = Estados.objects.all().order_by('id')
    context_object_name  = "Estados"
    pantalla_required    = '0009'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormEstados()           
        return ctx
    
    def get_queryset(self):
        return Estados.objects.filter(eliminado=False).order_by('id')

class EstadosCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Estados/CRUD/add.html'  
    model = Estados  
    form_class = FormEstados
    pantalla_required = '0009'
    success_url = reverse_lazy('estados:home_estados')  

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class EstadosEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Estados/CRUD/edit.html'  
    model = Estados  
    form_class = FormEstados
    pantalla_required = '0009'
    success_url = reverse_lazy('estados:home_estados')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class EstadosDelete(PantallaRequiredMixin, UpdateView):
    template_name      = 'Estados/CRUD/delete.html'
    model              = Estados
    form_class         = FormEstadosDELETE
    pantalla_required  = '0009'
    success_url        = reverse_lazy('estados:home_estados') 

    def post(self, request, pk):
        rol = get_object_or_404(Estados, pk=pk)
        rol.eliminado = True
        rol.save()
        return redirect(self.success_url)