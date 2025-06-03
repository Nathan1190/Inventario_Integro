from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import Proveedores
from roles.mixins import PantallaRequiredMixin

class ProveedoresList(PantallaRequiredMixin, ListView):
    template_name        = 'Proveedores/CRUD/index.html'
    queryset             = Proveedores.objects.all().order_by('id')
    context_object_name  = "Proveedores"
    pantalla_required    = '0010'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormProveedores()           
        return ctx
    
    def get_queryset(self):
        return Proveedores.objects.filter(eliminado=False).order_by('id')

class ProveedoresCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Proveedores/CRUD/add.html'  
    model = Proveedores  
    form_class = FormProveedores 
    pantalla_required = '0010'
    success_url = reverse_lazy('proveedores:home_proveedores')  

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class ProveedoresEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Proveedores/CRUD/edit.html'  
    model = Proveedores  
    form_class = FormProveedores
    pantalla_required = '0010'
    success_url = reverse_lazy('proveedores:home_proveedores')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class ProveedoresDelete(PantallaRequiredMixin, UpdateView):
    template_name      = 'Proveedores/CRUD/delete.html'
    model              = Proveedores
    form_class         = FormProveedoresDELETE
    pantalla_required  = '0010'
    success_url        = reverse_lazy('proveedores:home_proveedores') 

    def post(self, request, pk):
        rol = get_object_or_404(Proveedores, pk=pk)
        rol.eliminado = True
        rol.save()
        return redirect(self.success_url)