from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from .forms import FormCategorias, FormCategoriasDELETE
from .models import Categorias
from roles.mixins import PantallaRequiredMixin
import os

from django.http import JsonResponse


def categorias_por_objeto_gasto(request):
    objeto_gasto_id = request.GET.get("objeto_gasto_id")
    categorias = Categorias.objects.filter(objeto_gasto_id=objeto_gasto_id, eliminado=False).values("id", "nombre")
    return JsonResponse(list(categorias), safe=False)

class CategoriasList(PantallaRequiredMixin, ListView):
    template_name = 'Categorias/CRUD/index.html'
    queryset = Categorias.objects.all().order_by('id')
    context_object_name = 'Categorias'
    pantalla_required = '0012'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = FormCategorias()
        return ctx

    def get_queryset(self):
        return Categorias.objects.filter(eliminado=False).order_by('id')


class CategoriasCreate(PantallaRequiredMixin, CreateView):
    template_name = 'Categorias/CRUD/add.html'
    model = Categorias
    form_class = FormCategorias
    pantalla_required = '0012'
    success_url = reverse_lazy('categorias:home_categorias')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class CategoriasEdit(PantallaRequiredMixin, UpdateView):
    template_name = 'Categorias/CRUD/edit.html'
    model = Categorias
    form_class = FormCategorias
    pantalla_required = '0012'
    success_url = reverse_lazy('categorias:home_categorias')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class CategoriasDelete(PantallaRequiredMixin, UpdateView):
    template_name = 'Categorias/CRUD/delete.html'
    model = Categorias
    form_class = FormCategoriasDELETE
    pantalla_required = '0012'
    success_url = reverse_lazy('categorias:home_categorias')

    def post(self, request, pk):
        cat = get_object_or_404(Categorias, pk=pk)
        cat.eliminado = True
        cat.save()
        return redirect(self.success_url)


def export_categorias_pdf(request):
    """Exporta categorías a PDF con filtrado de columnas y paginado."""
    headers = ["ID", "Nombre", "Objeto de Gasto", "Descripción", "Creado", "Modificado"]
    fields = ["id", "nombre", "objeto_gasto", "descripcion", "creado_fecha", "fecha_de_modificacion"]

    cols_param = request.GET.get("cols", "")
    if cols_param:
        try:
            selected = [int(x) - 1 for x in cols_param.split(",") if x.strip()]
            selected = [i for i in selected if 0 <= i < len(headers)]
        except ValueError:
            selected = list(range(len(headers)))
    else:
        selected = list(range(len(headers)))

    qs = Categorias.objects.filter(eliminado=False).order_by("id")
    ids_param = request.GET.get("ids", "")
    if ids_param:
        try:
            ids = [int(i) for i in ids_param.split(",") if i.strip()]
            qs = qs.filter(id__in=ids)
        except ValueError:
            pass

    rows = []
    for cat in qs:
        row = []
        for i in selected:
            val = getattr(cat, fields[i])
            if i in (3, 4):
                val = val.strftime("%Y-%m-%d %H:%M")
            row.append(str(val))
        rows.append(row)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="categorias.pdf"'
    c = Canvas(response, pagesize=letter)
    width, height = letter
    per_page = 25
    page = 1

    logo_path = os.path.join(settings.BASE_DIR, "static/assets/img/logo.png")
    grey_logo = os.path.join(settings.BASE_DIR, "static/assets/img/logo_gris.png")
    bottom_text = os.path.join(settings.BASE_DIR, "static/assets/img/bottom_text.png")

    for start in range(0, len(rows), per_page):
        table_data = [[headers[i] for i in selected]] + rows[start:start + per_page]
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
        ]))

        if os.path.exists(grey_logo):
            c.drawImage(grey_logo, (width - 230) - 40, (height - 200) / 5, width=230, height=200, mask='auto')
        if os.path.exists(logo_path):
            c.drawImage(logo_path, (width - 316) / 2, height - 73 - 60, width=316, height=73, mask='auto')
        if os.path.exists(bottom_text):
            c.drawImage(bottom_text, (width - 400) / 2, (height - 50) / 15, width=400, height=50, mask='auto')

        c.setFillColor(CMYKColor(15, 0, 0, 0.4))
        c.rect(0, 0, width, 40, fill=1)

        user = request.user.get_full_name() or request.user.username
        c.setFont("Helvetica-Bold", 14)
        c.drawString((width - 150) / 2, height - 160, "Listado de Categorías")
        c.setFont("Helvetica", 10)
        c.drawString((width) / 8 , height - 30, f"Usuario: {user}")
        c.drawString(450, height - 30, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

        w, h = table.wrap(0, 0)
        x = (width - w) / 2
        y = (height - 180) - h
        table.drawOn(c, x, y)

        c.setFont("Helvetica", 9)
        c.setFillColor(colors.white)
        c.drawCentredString(width / 2, 20, f"Página {page}")
        page += 1
        c.showPage()

    c.save()
    return response
