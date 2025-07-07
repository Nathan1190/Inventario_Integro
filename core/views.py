from django.views.generic import View
from django.shortcuts import render

from django.db.models import Count
import json

from empleados.models import Empleados
from inventario.models import BienNacional
from proveedores.models import Proveedores
from dependencias.models import Dependencias
from asignaciones.models import AsignacionBien


class HomeView(View):
    def get(self, request, *args, **kwargs):
        count_bienes = BienNacional.objects.filter(eliminado=False).count()
        count_empleados = Empleados.objects.filter(eliminado=False).count()
        count_proveedores = Proveedores.objects.filter(eliminado=False).count()
        count_dependencias = Dependencias.objects.filter(eliminado=False).count()
        count_asignaciones = AsignacionBien.objects.count()

        category_counts = (
            BienNacional.objects.filter(eliminado=False)
            .values('categoria__nombre')
            .annotate(total=Count('id'))
            .order_by('categoria__nombre')
        )
        labels = [c['categoria__nombre'] or 'Sin categoría' for c in category_counts]
        values = [c['total'] for c in category_counts]

        context = {
            'count_bienes': count_bienes,
            'count_empleados': count_empleados,
            'count_proveedores': count_proveedores,
            'count_dependencias': count_dependencias,
            'count_asignaciones': count_asignaciones,
            'category_labels': json.dumps(labels),
            'category_values': json.dumps(values),
        }
        return render(request, 'Base/dashboard.html', context)
    
