import os
import re
from django.db.models import Count, Min, Max, Sum, F
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from .models import BienNacional, Manufacturera, Fabricante
from .forms import *
from roles.mixins import PantallaRequiredMixin
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime


# Generador automático del código UFTF-xxxxx
CODIGO_PREFIX = "UFTF-"
DIGITS = 5
codigo_regex = re.compile(rf"^{CODIGO_PREFIX}(\d{{{DIGITS}}})$")

def _siguiente_consecutivo():
    # Busca el mayor número usado hasta ahora
    max_code = (BienNacional.objects
        .filter(numero_inventario__startswith=CODIGO_PREFIX)
        .aggregate(max_num=Max('numero_inventario'))
    )['max_num']
    if max_code:
        # Extrae solo el número del código, por ejemplo, de UFTF-00123 saca 123
        try:
            last_num = int(max_code.replace(CODIGO_PREFIX, ""))
        except Exception:
            last_num = 0
        return last_num + 1
    else:
        return 0

def generar_codigos_para_bienes(cantidad):
    codigos = []
    consecutivo = _siguiente_consecutivo()  # Calcula el inicio solo una vez
    for i in range(cantidad):
        codigo = f"{CODIGO_PREFIX}{(consecutivo + i):0{DIGITS}d}"
        codigos.append(codigo)
    return codigos

class BienNacionalList(PantallaRequiredMixin, ListView):
    template_name = 'Inventario/CRUD/index.html'
    queryset = BienNacional.objects.filter(eliminado=False).order_by('nombre_bien')
    context_object_name = 'Bienes'
    pantalla_required = '0014'

    def get_queryset(self):
        qs = (
                BienNacional.objects
                .filter(eliminado=False)
                .values(
                    'nombre_bien',
                    'categoria',
                    'subcategoria',
                    'numero_modelo',
                    'compania',
                    'fabricante',
                    'manufacturera',
                    'unidad_medida'
                )
                .annotate(
                    min_id=Min('id'),
                    categoria_nombre=F('categoria__nombre'),
                    subcategoria_nombre=F('subcategoria__nombre'),
                    compania_nombre=F('compania__nombre'),
                    fabricante_nombre=F('fabricante__nombre'),
                    manufacturera_nombre=F('manufacturera__nombre'),
                    cantidad_total=Count('id'),
                    total=Count('total'),
                    disponibles=Sum('disponibles'),
                    costo_compra=Min('costo_compra'),
                )
                .order_by('nombre_bien')
             )
        # Luego, para cada grupo, busca el id con imagen no vacía
        for grupo in qs:
            bien_con_imagen = (
                BienNacional.objects
                .filter(
                    eliminado=False,
                    nombre_bien=grupo['nombre_bien'],
                    categoria=grupo['categoria'],
                    numero_modelo=grupo['numero_modelo'],
                    compania=grupo['compania'],
                    fabricante=grupo['fabricante'],
                    manufacturera=grupo['manufacturera'],
                    unidad_medida=grupo['unidad_medida'],
                )
                .exclude(imagen="")
                .exclude(imagen__isnull=True)
                .first()
            )
            grupo['imagen_url'] = bien_con_imagen.imagen.url if (bien_con_imagen and bien_con_imagen.imagen) else None
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = BienNacionalForm()
        ctx['manufacturera_form'] = ManufactureraForm()
        ctx['compania_form'] = CompaniaForm() 
        ctx['fabricante_form'] = FabricanteForm()
        return ctx

class BienNacionalCreate(PantallaRequiredMixin, UpdateView):
    template_name = 'Inventario/CRUD/add.html'
    model = BienNacional
    form_class = BienNacionalForm
    pantalla_required = '0014'
    success_url = reverse_lazy('inventario:home_bienesnacionales')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'manufacturera_form': ManufactureraForm(),
            'compania_form': ManufactureraForm(),
            'fabricante_form': FabricanteForm(),
        })

    def post(self, request, *args, **kwargs):
        # Crear manufacturera
        if 'crear_manufacturera' in request.POST:
            manufacturera_form = ManufactureraForm(request.POST)
            form = self.form_class()
            if manufacturera_form.is_valid():
                manufacturera_form.save()
                return render(request, self.template_name, {
                    'form': form,
                    'manufacturera_form': ManufactureraForm(),
                    'compania_form': ManufactureraForm(),
                    'fabricante_form': FabricanteForm(),
                    'manufacturera_added': True
                })
            return render(request, self.template_name, {
                'form': form,
                'manufacturera_form': manufacturera_form,
                'compania_form': ManufactureraForm(),
                'fabricante_form': FabricanteForm(),
            })

        # Crear compañía (usa el mismo form y modelo que manufacturera)
        if 'crear_compania' in request.POST:
            compania_form = CompaniaForm(request.POST)
            form = self.form_class()
            if compania_form.is_valid():
                compania_form.save()
                return render(request, self.template_name, {
                    'form': form,
                    'compania_form': CompaniaForm(),
                    'compania_form': CompaniaForm(),
                    'fabricante_form': FabricanteForm(),
                    'compania_added': True
                })
            return render(request, self.template_name, {
                'form': form,
                'compania_form': CompaniaForm(),
                'fabricante_form': FabricanteForm(),
            })

        # Crear fabricante
        if 'crear_fabricante' in request.POST:
            fabricante_form = FabricanteForm(request.POST)
            form = self.form_class()
            if fabricante_form.is_valid():
                fabricante_form.save()
                return render(request, self.template_name, {
                    'form': form,
                    'manufacturera_form': ManufactureraForm(),
                    'compania_form': ManufactureraForm(),
                    'fabricante_form': FabricanteForm(),
                    'fabricante_added': True
                })
            return render(request, self.template_name, {
                'form': form,
                'manufacturera_form': ManufactureraForm(),
                'compania_form': ManufactureraForm(),
                'fabricante_form': fabricante_form,
            })

        # Crear Bien Nacional normal
        form = self.form_class(request.POST, request.FILES)
        manufacturera_form = ManufactureraForm()
        compania_form = ManufactureraForm()
        fabricante_form = FabricanteForm()
        if form.is_valid():
            cantidad = int(request.POST.get('total', 1)) or 1
            codigos = generar_codigos_para_bienes(cantidad)
            with transaction.atomic():
                for i in range(cantidad):
                    bien = form.save(commit=False)
                    bien.pk = None
                    bien.numero_inventario = codigos[i]
                    if 'imagen' in request.FILES and i > 0:
                        bien.imagen = None
                    bien.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {
            'form': form,
            'manufacturera_form': manufacturera_form,
            'compania_form': compania_form,
            'fabricante_form': fabricante_form,
        })

def export_inventario_pdfv(request):
    """Exporta inventareio a PDF con filtrado de columnas y paginado."""
    headers = ["ID", "Imagen", "Numero de Inventario", "Nombre", "Categoria", "Subcategoria", "Compañía", "Manufacturera", "Fabricante", "Proveedor", "Serial", "Tamaño", "Modelo", "Ubicación", "Estado", "Tota", "Disponibles", "Cantidad Minima",  "Numero de Orden", "Numero de Factura", "Responsable", "Costo de Compra",  "Fecha de Compra", "Creado", "Modificado"]
    fields = ["id", "imagen", "numero_inventario", "nombre_bien", "categoria", "subcategoria", "compania", "manufacturera", "fabricante", "proveedor", "serial", "unidad_medida", "numero_modelo", "ubicacion", "estado_fisico", "total", "disponibles", "cantidad_minima", "numero_orden", "numero_factura", "responsable", "costo_compra", "fecha_compra", "creado", "modificado"]

    cols_param = request.GET.get("cols", "")
    if cols_param:
        try:
            selected = [int(x) - 1 for x in cols_param.split(",") if x.strip()]
            selected = [i for i in selected if 0 <= i < len(headers)]
        except ValueError:
            selected = list(range(len(headers)))
    else:
        selected = list(range(len(headers)))

    qs = BienNacional.objects.filter(eliminado=False).order_by("id")
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
            if i in (22, 23, 24):
                val = val.strftime("%Y-%m-%d %H:%M")
            row.append(str(val))
        rows.append(row)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="inventario.pdf"'
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
        c.drawString((width - 150) / 2, height - 160, "Listado de Inventario")
        c.setFont("Helvetica", 10)
        c.drawString((width) / 8 , height - 30, f"Usuario: {user}")
        c.drawString(450, height - 30, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

        w, h = table.wrap(0, 0)
        x = (width - w) / 2
        y = (height - 180) - h
        table.drawOn(c, x, y)

         # <--- AQUI pega la suma total (solo la última página idealmente)
    if start + per_page >= len(rows):  # Última página
        # Sumar costo_compra de todos los rows (except header)
        indice_costo = fields.index('costo_compra')
        total_costo = 0
        for row in rows:
            try:
                total_costo += float(row[indice_costo].replace('L.', '').replace(',', '').strip())
            except Exception:
                pass
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.black)
        c.drawRightString(width - 50, y - 18, f"Total general de Costo de Compra: L. {total_costo:,.2f}")


        c.setFont("Helvetica", 9)
        c.setFillColor(colors.white)
        c.drawCentredString(width / 2, 20, f"Página {page}")
        page += 1
        c.showPage()

    c.save()
    return response

def export_inventario_pdfh(request):
    """Exporta inventareio a PDF con filtrado de columnas y paginado."""
    headers = ["ID", "Imagen", "Numero de Inventario", "Nombre", "Categoria", "Subcategoria", "Compañía", "Manufacturera", "Fabricante", "Proveedor", "Serial", "Tamaño", "Modelo", "Ubicación", "Estado", "Tota", "Disponibles", "Cantidad Minima",  "Numero de Orden", "Numero de Factura", "Responsable", "Costo de Compra",  "Fecha de Compra", "Creado", "Modificado"]
    fields = ["id", "imagen", "numero_inventario", "nombre_bien", "categoria", "subcategoria", "compania", "manufacturera", "fabricante", "proveedor", "serial", "unidad_medida", "numero_modelo", "ubicacion", "estado_fisico", "total", "disponibles", "cantidad_minima", "numero_orden", "numero_factura", "responsable", "costo_compra", "fecha_compra", "creado", "modificado"]

    cols_param = request.GET.get("cols", "")
    if cols_param:
        try:
            selected = [int(x) - 1 for x in cols_param.split(",") if x.strip()]
            selected = [i for i in selected if 0 <= i < len(headers)]
        except ValueError:
            selected = list(range(len(headers)))
    else:
        selected = list(range(len(headers)))

    qs = BienNacional.objects.filter(eliminado=False).order_by("id")
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
            if i in (22, 23, 24):
                val = val.strftime("%Y-%m-%d %H:%M")
            row.append(str(val))
        rows.append(row)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="inventario.pdf"'
    ca = Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)
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
            ca.drawImage(grey_logo, (width - 230) - 40, (height - 200) / 5, width=230, height=200, mask='auto')
        if os.path.exists(logo_path):
            ca.drawImage(logo_path, (width - 316) / 2, height - 73 - 60, width=316, height=73, mask='auto')
        if os.path.exists(bottom_text):
            ca.drawImage(bottom_text, (width - 400) / 2, (height - 50) / 15, width=400, height=50, mask='auto')

        ca.setFillColor(CMYKColor(15, 0, 0, 0.4))
        ca.rect(0, 0, width, 40, fill=1)

        user = request.user.get_full_name() or request.user.username
        ca.setFont("Helvetica-Bold", 14)
        ca.drawString((width - 150) / 2, height - 160, "Listado de Inventario")
        ca.setFont("Helvetica", 10)
        ca.drawString((width) / 8 , height - 30, f"Usuario: {user}")
        ca.drawString((width) / 1.3, height - 30, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

        w, h = table.wrap(0, 0)
        x = (width - w) / 2
        y = (height - 180) - h
        table.drawOn(ca, x, y)

        ca.setFont("Helvetica", 9)
        ca.setFillColor(colors.white)
        ca.drawCentredString(width / 2, 20, f"Página {page}")
        page += 1
        ca.showPage()

    ca.save()
    return response