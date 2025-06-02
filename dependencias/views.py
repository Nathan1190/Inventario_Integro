from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from roles.mixins import PantallaRequiredMixin

class DependenciasList(PantallaRequiredMixin, ListView):
    template_name        = 'Dependencias/CRUD/index.html'
    queryset             = Dependencias.objects.all().order_by('id')
    context_object_name  = "Dependencias"
    pantalla_required    = '0005'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormDependencias()           
        return ctx
    
    def get_queryset(self):
        return Dependencias.objects.filter(eliminado=False).order_by('id')

class DependenciasCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Dependencias/CRUD/add.html'  
    model = Dependencias  
    form_class = FormDependencias
    pantalla_required = '0005'
    success_url = reverse_lazy('dependencias:home_dependencias')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class DependenciasEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Dependencias/CRUD/edit.html'  
    model = Dependencias  
    form_class = FormDependencias
    pantalla_required = '0005'
    success_url = reverse_lazy('dependencias:home_dependencias')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class DependenciasDelete(PantallaRequiredMixin, UpdateView):
    template_name      = 'Dependencias/CRUD/delete.html'
    model              = Dependencias
    form_class         = FormDependenciasDELETE
    pantalla_required  = '0005'
    success_url        = reverse_lazy('dependencias:home_dependencias') 

    def post(self, request, pk):
        rol = get_object_or_404(Dependencias, pk=pk)
        rol.eliminado = True
        rol.save()
        return redirect(self.success_url)