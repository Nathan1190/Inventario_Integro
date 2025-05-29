from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from roles.mixins import PantallaRequiredMixin

class EmpleadosList(PantallaRequiredMixin, ListView):
    template_name        = 'Empleados/CRUD/index.html'
    queryset             = Empleados.objects.all().order_by('id')
    context_object_name  = "Empleados"
    pantalla_required    = '0002'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormEmpleados()           
        return ctx
    
    def get_queryset(self):
        return Empleados.objects.filter(eliminado=False).order_by('id')

class EmpleadosCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Empleados/CRUD/add.html'  
    model = Empleados  
    form_class = FormEmpleados 
    pantalla_required = '0002'
    success_url = reverse_lazy('empleados:home_empleados')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class EmpleadosEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Empleados/CRUD/edit.html'  
    model = Empleados  
    form_class = FormEmpleados
    pantalla_required = '0002'
    success_url = reverse_lazy('empleados:home_empleados')  

    def form_valid(self, form):
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return render(self.request, self.template_name, {'form': form})

class EmpleadosDelete(PantallaRequiredMixin, UpdateView):
    template_name      = 'Empleados/CRUD/delete.html'
    model              = Empleados
    form_class         = FormEmpleadosDELETE
    pantalla_required  = '0002'
    success_url        = reverse_lazy('empleados:home_empleados') 

    def post(self, request, pk):
        rol = get_object_or_404(Empleados, pk=pk)
        rol.eliminado = True
        rol.save()
        return redirect(self.success_url)