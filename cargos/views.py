from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from roles.mixins import PantallaRequiredMixin

class CargosList(PantallaRequiredMixin, ListView):
    template_name        = 'Cargos/CRUD/index.html'
    queryset             = Cargos.objects.all().order_by('id')
    context_object_name  = "Cargos"
    pantalla_required    = '0004'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormCargos()           
        return ctx
    
    def get_queryset(self):
        return Cargos.objects.filter(eliminado=False).order_by('id')

class CargosCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Cargos/CRUD/add.html'  
    model = Cargos  
    form_class = FormCargos
    pantalla_required = '0004'
    success_url = reverse_lazy('cargos:home_cargos')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class CargosEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Cargos/CRUD/edit.html'  
    model = Cargos  
    form_class = FormCargos
    pantalla_required = '0004'
    success_url = reverse_lazy('cargos:home_cargos')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class CargosDelete(PantallaRequiredMixin, UpdateView):
    template_name      = 'Cargos/CRUD/delete.html'
    model              = Cargos
    form_class         = FormCargosDELETE
    pantalla_required  = '0004'
    success_url        = reverse_lazy('cargos:home_cargos') 

    def post(self, request, pk):
        rol = get_object_or_404(Cargos, pk=pk)
        rol.eliminado = True
        rol.save()
        return redirect(self.success_url)