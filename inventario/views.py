import os
import re
from django.db.models import Count, Min, Max, Sum, F
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from .models import *
from .forms import *
from roles.mixins import PantallaRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def bienes_por_filtros(request):
    objeto_gasto_id = request.GET.get("objeto_gasto_id")
    categoria_id = request.GET.get("categoria_id")
    subcategoria_id = request.GET.get("subcategoria_id")
    queryset = BienNacional.objects.filter(eliminado=False)

    if objeto_gasto_id:
        queryset = queryset.filter(objeto_gasto_id=objeto_gasto_id)
    if categoria_id:
        queryset = queryset.filter(categoria_id=categoria_id)
    if subcategoria_id:
        queryset = queryset.filter(subcategoria_id=subcategoria_id)
    bienes = queryset.values("id", "nombre_bien", "numero_inventario")
    response = [
        {"id": b["id"], "label": f'{b["numero_inventario"]} - {b["nombre_bien"]}'}
        for b in bienes
    ]
    return JsonResponse(response, safe=False)


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

@csrf_exempt
def agregar_mas_bienes(request):
    if request.method == 'POST':
        nombre_bien = request.POST.get('nombre_bien')
        objeto_gasto_id = request.POST.get('objeto_gasto')
        categoria_id = request.POST.get('categoria')
        subcategoria_id = request.POST.get('subcategoria') or None
        cantidad = int(request.POST.get('cantidad', 1))

        # Busca un bien base para copiar todos los campos
        bien_base = BienNacional.objects.filter(
            nombre_bien=nombre_bien,
            objeto_gasto_id=objeto_gasto_id,
            categoria_id=categoria_id,
            subcategoria_id=subcategoria_id,
        ).first()

        if not bien_base:
            return JsonResponse({'ok': False, 'error': 'Bien base no encontrado.'}, status=400)

        # Genera los nuevos códigos
        codigos = generar_codigos_para_bienes(cantidad)
        nuevos_bienes = []
        for i in range(cantidad):
            bien = BienNacional(
                imagen=None,  
                compania=bien_base.compania,
                nombre_bien=bien_base.nombre_bien,
                objeto_gasto=bien_base.objeto_gasto,
                categoria=bien_base.categoria,
                subcategoria=bien_base.subcategoria,
                numero_modelo=bien_base.numero_modelo,
                manufacturera=bien_base.manufacturera,
                fabricante=bien_base.fabricante,
                proveedor=bien_base.proveedor,
                serial='',  
                numero_inventario=codigos[i],
                unidad_medida=bien_base.unidad_medida,
                ubicacion=bien_base.ubicacion,
                fecha_compra=bien_base.fecha_compra,
                costo_compra=bien_base.costo_compra,
                numero_orden=bien_base.numero_orden,
                numero_factura=bien_base.numero_factura,
                notas=bien_base.notas,
            )
            bien.save()
            bien.estado_fisico.set(bien_base.estado_fisico.all())  # Copia los estados físicos
            nuevos_bienes.append(bien)
        return JsonResponse({'ok': True, 'msg': f'{cantidad} bienes agregados.'})
    return JsonResponse({'ok': False, 'error': 'Método no permitido.'}, status=405)

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
                    'objeto_gasto',
                    'categoria',
                    'subcategoria',
                )
                .annotate(
                    min_id=Min('id'),
                    objeto_gasto_nombre=F('objeto_gasto__nombre'),
                    categoria_nombre=F('categoria__nombre'),
                    subcategoria_nombre=F('subcategoria__nombre'),
                    compania_nombre=F('compania__nombre'),
                )
                .order_by('nombre_bien')
             )
        # Luego, para cada grupo, busca el id con imagen no vacía
        imagenes = {}
        for grupo in qs:
            clave = (grupo['nombre_bien'], grupo['objeto_gasto'], grupo['categoria'], grupo['subcategoria'])
            if clave not in imagenes:
                bien_con_imagen = (
                    BienNacional.objects
                    .filter(
                        eliminado=False,
                        nombre_bien=grupo['nombre_bien'],
                        objeto_gasto=grupo['objeto_gasto'],
                        categoria=grupo['categoria'],
                        subcategoria=grupo['subcategoria'],
                    )
                    .exclude(imagen="")
                    .exclude(imagen__isnull=True)
                    .first()
                )
            imagenes[clave] = bien_con_imagen.imagen.url if (bien_con_imagen and bien_con_imagen.imagen) else None
            grupo['imagen_url'] = imagenes[clave]
            stock = StockBien.objects.filter(
                nombre_bien=grupo['nombre_bien'],
                objeto_gasto_id=grupo['objeto_gasto'],
                categoria_id=grupo['categoria'],
                subcategoria_id=grupo['subcategoria'],
            ).first()
            grupo['cantidad_minima'] = stock.cantidad_minima if stock else 0
            grupo['cantidad_restante'] = stock.cantidad_restante if stock else 0
            grupo['total_asignado'] = stock.total_asignado if stock else 0
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
            'compania_form': CompaniaForm(),
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
                    'compania_form': CompaniaForm(),
                    'fabricante_form': FabricanteForm(),
                    'manufacturera_added': True
                })
            return render(request, self.template_name, {
                'form': form,
                'manufacturera_form': manufacturera_form,
                'compania_form': CompaniaForm(),
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
                    'compania_form': CompaniaForm(),
                    'fabricante_form': FabricanteForm(),
                    'fabricante_added': True
                })
            return render(request, self.template_name, {
                'form': form,
                'manufacturera_form': ManufactureraForm(),
                'compania_form': CompaniaForm(),
                'fabricante_form': fabricante_form,
            })

        # Crear Bien Nacional normal
        form = self.form_class(request.POST, request.FILES)
        manufacturera_form = ManufactureraForm()
        compania_form = CompaniaForm()
        fabricante_form = FabricanteForm()
        if form.is_valid():
            total = form.cleaned_data['total_bienes']
            cantidad_minima = form.cleaned_data['cantidad_minima'] or 0
            codigos = generar_codigos_para_bienes(total)
            bienes = []
            with transaction.atomic():
                for i in range(total):
                    bien = form.save(commit=False)
                    bien.pk = None
                    bien.numero_inventario = codigos[i]
                    if 'imagen' in request.FILES and i > 0:
                        bien.imagen = None
                    bien.save()
                    bienes.append(bien)
            # Solo después de guardar todos los bienes, actualizamos o creamos el stock
            bien_ref = bienes[0]
            stock, created = StockBien.objects.get_or_create(
                nombre_bien=bien_ref.nombre_bien,
                objeto_gasto=bien_ref.objeto_gasto,
                categoria=bien_ref.categoria,
                subcategoria=bien_ref.subcategoria,
            )

            # Total = todos los bienes de ese tipo (sin eliminar)
            total = BienNacional.objects.filter(
                nombre_bien=bien_ref.nombre_bien,
                objeto_gasto=bien_ref.objeto_gasto,
                categoria=bien_ref.categoria,
                subcategoria=bien_ref.subcategoria,
                eliminado=False,
            ).count()

            # Restantes = los bienes NO asignados (responsable es NULL)
            cantidad_restante = BienNacional.objects.filter(
                nombre_bien=bien_ref.nombre_bien,
                objeto_gasto=bien_ref.objeto_gasto,
                categoria=bien_ref.categoria,
                subcategoria=bien_ref.subcategoria,
                responsable__isnull=True,
                eliminado=False,
            ).count()

            stock.total = total
            stock.cantidad_minima = cantidad_minima
            stock.cantidad_restante = cantidad_restante
            stock.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {
            'form': form,
            'manufacturera_form': manufacturera_form,
            'compania_form': compania_form,
            'fabricante_form': fabricante_form,
        })
    
    def form_valid(self, form):
        total = form.cleaned_data['total_bienes']
        cantidad_minima = form.cleaned_data['cantidad_minima'] or 0
        # Guarda la cantidad de bienes individualmente
        bienes = []
        for i in range(total):
            bien = form.save(commit=False)
            if i > 0:
                bien.pk = None  # Fuerza un nuevo registro
                bien.imagen = None  # Solo sube la imagen en el primero
            bien.save()
            bienes.append(bien)
        return redirect(self.success_url)

def export_inventario_pdfv(request):
        """Exporta inventareio a PDF con filtrado de columnas y paginado."""
        headers = [
        "Imagen", "Nombre del Bien", "Categoría", "Subcategoría", "Fabricante", "Proveedor", "Total", "Disponible", "Cantidad Mínima"
        ]
        fields = [
        "imagen", "nombre_bien", "objeto_gasto", "categoria", "subcategoria",
        "fabricante", "proveedor", "total_asignado", "cantidad_restante", "cantidad_minima"
        ]
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
            stock = StockBien.objects.filter(
                nombre_bien=cat.nombre_bien,
                objeto_gasto=cat.objeto_gasto,
                categoria=cat.categoria,
                subcategoria=cat.subcategoria
            ).first()
            total_asignado = stock.total_asignado if stock else 0
            cantidad_restante = stock.cantidad_restante if stock else 0
            cantidad_minima = stock.cantidad_minima if stock else 0

            row = []
            for i in selected:
                field = fields[i]
                if field == "total_asignado":
                    val = total_asignado
                elif field == "cantidad_restante":
                    val = cantidad_restante
                elif field == "cantidad_minima":
                    val = cantidad_minima
                else:
                    val = getattr(cat, field)
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
        #if start + per_page >= len(rows):  # Última página
        # Sumar costo_compra de todos los rows (except header)
        #indice_costo = fields.index('costo_compra')
        #total_costo = 0
        #for row in rows:
        #    try:
        #        total_costo += float(row[indice_costo].replace('L.', '').replace(',', '').strip())
        #    except Exception:
        #        pass
        #c.setFont("Helvetica-Bold", 11)
        #c.setFillColor(colors.black)
        #c.drawRightString(width - 50, y - 18, f"Total general de Costo de Compra: L. {total_costo:,.2f}")


            c.setFont("Helvetica", 9)
            c.setFillColor(colors.white)
            c.drawCentredString(width / 2, 20, f"Página {page}")
            page += 1
            c.showPage()

        c.save()
        return response

def export_inventario_pdfh(request):
    """Exporta inventareio a PDF con filtrado de columnas y paginado."""
    headers = [
    "Imagen", "Nombre del Bien", "Objeto de Gasto", "Categoría", "Subcategoría", "Fabricante", "Proveedor", "Total", "Disponible", "Cantidad Mínima"
    ]
    fields = [
    "imagen", "nombre_bien", "objeto_gasto", "categoria", "subcategoria",
    "fabricante", "proveedor", "total_asignado", "cantidad_restante", "cantidad_minima"
    ]
    
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
        stock = StockBien.objects.filter(
            nombre_bien=cat.nombre_bien,
            objeto_gasto=cat.objeto_gasto,
            categoria=cat.categoria,
            subcategoria=cat.subcategoria
        ).first()
        total_asignado = stock.total_asignado if stock else 0
        cantidad_restante = stock.cantidad_restante if stock else 0
        cantidad_minima = stock.cantidad_minima if stock else 0

        row = []
        for i in selected:
            field = fields[i]
            if field == "total_asignado":
                val = total_asignado
            elif field == "cantidad_restante":
                val = cantidad_restante
            elif field == "cantidad_minima":
                val = cantidad_minima
            else:
                val = getattr(cat, field)
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


def buscar_por_numero_inventario(request):
    numero = request.GET.get("numero", "").strip()
    bien = BienNacional.objects.filter(numero_inventario__iexact=numero, eliminado=False).first()
    if not bien:
        return JsonResponse({"ok": False, "msg": "No se encontró el bien."})

    return JsonResponse({
        "ok": True,
        "nombre_bien": bien.nombre_bien,
        "objeto_gasto_id": bien.objeto_gasto.id if bien.objeto_gasto else None,
        "categoria_id": bien.categoria.id if bien.categoria else None,
        "subcategoria_id": bien.subcategoria.id if bien.subcategoria else 0,
        "url_desagrupado": reverse_lazy(
            "bien_detalle:desagrupado",
            kwargs={
                "nombre_bien": bien.nombre_bien,
                "objeto_gasto_id": bien.objeto_gasto.id if bien.objeto_gasto else 0,
                "categoria_id": bien.categoria.id if bien.categoria else 0,
                "subcategoria_id": bien.subcategoria.id if bien.subcategoria else 0,
            }
        ),
        "bien_id": bien.id
    })