import os
from django.shortcuts import redirect
from django.views.generic import ListView
from inventario.models import BienNacional
from django.views.generic import ListView, UpdateView
from inventario.models import BienNacional
from inventario.forms import BienNacionalEditForm
from .forms import *
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import letter, landscape, legal
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle
from inventario.models import StockBien
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from datetime import datetime
from roles.mixins import PantallaRequiredMixin

class BienDetalleList(PantallaRequiredMixin, ListView):
    template_name = "BienDetalle/desagrupado.html"
    context_object_name = "bienes"
    pantalla_required = '0019'

    def get_queryset(self):
        
        nombre_bien = self.kwargs['nombre_bien']
        objeto_gasto_id = self.kwargs['objeto_gasto_id']
        categoria_id = self.kwargs['categoria_id']
        subcategoria_id = self.kwargs['subcategoria_id']
        return BienNacional.objects.filter(
            eliminado=False,
            nombre_bien=nombre_bien,
            objeto_gasto_id=objeto_gasto_id,
            categoria_id=categoria_id,
            subcategoria_id=subcategoria_id
        ).order_by('id')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['nombre_bien'] = self.kwargs['nombre_bien']
        ctx['objeto_gasto_id'] = self.kwargs['objeto_gasto_id']
        ctx['categoria_id'] = self.kwargs['categoria_id']
        ctx['subcategoria_id'] = self.kwargs['subcategoria_id']

        # Lógica de imagen heredada
        bienes = list(ctx['bienes'])  # Es el queryset
        # Busca la primera imagen disponible en el grupo
        bien_con_imagen = None
        for bien in bienes:
            if bien.imagen:
                bien_con_imagen = bien
                break
        imagen_grupo = bien_con_imagen.imagen.url if bien_con_imagen and bien_con_imagen.imagen else None

        # Asigna imagen_mostrar a cada bien
        for bien in bienes:
            bien.imagen_mostrar = bien.imagen.url if bien.imagen else imagen_grupo

        # AHORA ACTUALIZA EL CONTEXTO CON LA LISTA
        ctx['bienes'] = bienes

        return ctx 
    
def export_inventario_pdfv(request, nombre_bien, objeto_gasto_id, categoria_id, subcategoria_id):
        """Exporta inventareio a PDF con filtrado de columnas y paginado."""
        headers = ["Id", "Numero de Inventario", "Imagen", "Nombre del Bien", "Objeto de Gasto", "Categoría", "Subcategoría", "Compañia", "Manufacturera", "Fabricante", "Proveedor", "Serial", "Modelo", "Unidad de Medida", "Ubicacion", "Numero de Orden", "Numero de Factura", "Costo de Compra", "Fecha de Compra", "Estados", "Responsable", "Notas", "Fecha de Creado", "Fecha de Modificado"]
        fields = ["id", "numero_inventario", "imagen_mostrar", "nombre_bien", "objeto_gasto", "categoria", "subcategoria", "compania", "manufacturera", "fabricante", "proveedor", "serial", "numero_modelo", "unidad_medida", "ubicacion", "numero_orden", "numero_factura", "costo_compra", "fecha_compra", "estado", "responsable", "notas", "creado", "modificado"]
        cols_param = request.GET.get("cols", "")
        if cols_param:
            try:
                selected = [int(x) - 1 for x in cols_param.split(",") if x.strip()]
                selected = [i for i in selected if 0 <= i < len(headers)]
            except ValueError:
                selected = list(range(len(headers)))
        else:
            selected = list(range(len(headers)))

        qs = BienNacional.objects.filter(eliminado=False,nombre_bien=nombre_bien,objeto_gasto_id=objeto_gasto_id,categoria_id=categoria_id,subcategoria_id=subcategoria_id).order_by("id")
        ids_param = request.GET.get("ids", "")
        if ids_param:
            try:
                ids = [int(i) for i in ids_param.split(",") if i.strip()]
                qs = qs.filter(id__in=ids)
            except ValueError:
                pass
        
        
        total_costo = 0
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
                if field == "costo_compra":
                    val = getattr(cat, "costo_compra", 0) or 0
                    # SUMA AQUÍ en vez de después
                    try:
                        total_costo += float(val)
                    except Exception:
                        pass
                    val = f"L. {float(val):,.2f}" if val else ""
                if field == "total_asignado":
                    val = total_asignado
                elif field == "cantidad_restante":
                    val = cantidad_restante
                elif field == "cantidad_minima":
                    val = cantidad_minima
                elif field == "estado":
                    estados = cat.estado_fisico.all()
                    if estados:
                        val = ', '.join([f"{e.nombre}" if e.color_hex else e.nombre for e in estados])
                    else:
                        val = "Sin estado"
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

            if start + per_page >= len(rows):  
                if total_costo > 0:
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

def export_inventario_pdfh(request, nombre_bien, objeto_gasto_id, categoria_id, subcategoria_id):
        """Exporta inventareio a PDF con filtrado de columnas y paginado."""
        headers = ["Id", "Numero de Inventario", "Imagen", "Nombre del Bien", "Objeto de Gasto", "Categoría", "Subcategoría", "Compañia", "Manufacturera", "Fabricante", "Proveedor", "Serial", "Modelo", "Unidad de Medida", "Ubicacion", "Numero de Orden", "Numero de Factura", "Costo de Compra", "Fecha de Compra", "Estados", "Responsable", "Notas", "Fecha de Creado", "Fecha de Modificado"]
        fields = ["id", "numero_inventario", "imagen_mostrar", "nombre_bien", "objeto_gasto", "categoria", "subcategoria", "compania", "manufacturera", "fabricante", "proveedor", "serial", "numero_modelo", "unidad_medida", "ubicacion", "numero_orden", "numero_factura", "costo_compra", "fecha_compra", "estado", "responsable", "notas", "creado", "modificado"]
    
        cols_param = request.GET.get("cols", "")
        if cols_param:
            try:
                selected = [int(x) - 1 for x in cols_param.split(",") if x.strip()]
                selected = [i for i in selected if 0 <= i < len(headers)]
            except ValueError:
                selected = list(range(len(headers)))
        else:
            selected = list(range(len(headers)))

        qs = BienNacional.objects.filter(eliminado=False,nombre_bien=nombre_bien,objeto_gasto_id=objeto_gasto_id,categoria_id=categoria_id,subcategoria_id=subcategoria_id).order_by("id")
        ids_param = request.GET.get("ids", "")
        if ids_param:
            try:
                ids = [int(i) for i in ids_param.split(",") if i.strip()]
                qs = qs.filter(id__in=ids)
            except ValueError:
                pass

        total_costo = 0
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
                if field == "costo_compra":
                    val = getattr(cat, "costo_compra", 0) or 0
                    # SUMA AQUÍ en vez de después
                    try:
                        total_costo += float(val)
                    except Exception:
                        pass
                    val = f"L. {float(val):,.2f}" if val else ""
                if field == "total_asignado":
                    val = total_asignado
                elif field == "cantidad_restante":
                    val = cantidad_restante
                elif field == "cantidad_minima":
                    val = cantidad_minima
                elif field == "estado":
                    estados = cat.estado_fisico.all()
                    if estados:
                        val = ', '.join([f"{e.nombre}" if e.color_hex else e.nombre for e in estados])
                    else:
                        val = "Sin estado"
                else:
                    val = getattr(cat, field)
                row.append(str(val))
            rows.append(row)
            

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'filename="inventario.pdf"'
        ca = Canvas(response, pagesize=landscape(legal))
        width, height = landscape(legal)
        per_page = 25
        page = 1

        logo_path = os.path.join(settings.BASE_DIR, "static/assets/img/logo.png")
        grey_logo = os.path.join(settings.BASE_DIR, "static/assets/img/logo_gris.png")
        bottom_text = os.path.join(settings.BASE_DIR, "static/assets/img/bottom_text.png")

        for start in range(0, len(rows), per_page):
            table_data = [[headers[i] for i in selected]] + rows[start:start + per_page]
            table = Table(table_data)
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

            if start + per_page >= len(rows):  
                if total_costo > 0:
                    ca.setFont("Helvetica-Bold", 11)
                    ca.setFillColor(colors.black)
                    ca.drawRightString(width - 65, y - 18, f"Total general de Costo de Compra: L. {total_costo:,.2f}")


            ca.setFont("Helvetica", 9)
            ca.setFillColor(colors.white)
            ca.drawCentredString(width / 2, 20, f"Página {page}")
            page += 1
            ca.showPage()

        ca.save()
        return response



    
class BienDetalleEdit(PantallaRequiredMixin, UpdateView):
    
    model = BienNacional
    form_class = BienNacionalEditForm
    template_name = "BienDetalle/edit.html"
    pantalla_required = '0019'

    class Meta:
        model = BienNacional
        exclude = [
            'eliminado', 'creado', 'modificado',
            'total_asignado', 'cantidad_restante', 'responsable',
        ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'total_bienes' in form.fields:
            del form.fields['total_bienes']
        if 'cantidad_minima' in form.fields:
            form.fields['cantidad_minima'].required = False
        return form

    def get_success_url(self):
        bien = self.object
        return reverse_lazy(
            'bien_detalle:desagrupado',
            kwargs={
                'nombre_bien': bien.nombre_bien,
                'objeto_gasto_id': bien.objeto_gasto.id,
                'categoria_id': bien.categoria.id,
                'subcategoria_id': bien.subcategoria.id if bien.subcategoria else 0
            }
        )
    
    def form_valid(self, form):
        if not form.cleaned_data.get('responsable'):
            form.instance.responsable = self.get_object().responsable
        return super().form_valid(form)


    def form_invalid(self, form):
        print("Errores del formulario:", form.errors)  # Esto imprime los errores en tu consola de Django
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class BienDetalleDelete(UpdateView):
    model = BienNacional
    template_name = "BienDetalle/delete.html"
    form_class = BienNacionalDeleteForm

    def post(self, request, *args, **kwargs):
        bien = self.get_object()
        bien.eliminado = True
        bien.save()
        # Redirige al desagrupado (puedes mejorar la UX con mensajes)
        return redirect('bien_detalle:desagrupado',
            nombre_bien=bien.nombre_bien,
            objeto_gasto_id=bien.objeto_gasto.id,
            categoria_id=bien.categoria.id,
            subcategoria_id=bien.subcategoria.id if bien.subcategoria else 0
        )
