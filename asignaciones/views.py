from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from roles.mixins import PantallaRequiredMixin
from .models import AsignacionBien
from .forms import AsignacionBienForm
from inventario.models import BienNacional
from django.contrib import messages
import os
from empleados.models import Empleados

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
from django.conf import settings
from datetime import datetime

class AsignacionBienListView(PantallaRequiredMixin, ListView):
    template_name = 'Asignaciones/lista.html'
    model = AsignacionBien
    context_object_name = 'asignaciones'
    pantalla_required = '0020'  # Define tu código de permiso

    def get_queryset(self):
        return AsignacionBien.objects.select_related('bien', 'responsable').order_by('-fecha_asignacion')

class AsignarBienCreateView(PantallaRequiredMixin, CreateView):
    template_name = 'Asignaciones/asignar.html'
    model = AsignacionBien
    form_class = AsignacionBienForm
    pantalla_required = '0020'

    def dispatch(self, request, *args, **kwargs):
        self.bien = get_object_or_404(BienNacional, pk=kwargs['bien_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['bien'] = self.bien
        # Buscar asignación pendiente
        asignacion_pendiente = AsignacionBien.objects.filter(
            bien=self.bien, estado='pendiente'
        ).first()
        ctx['asignacion_pendiente'] = asignacion_pendiente
        return ctx

    def form_valid(self, form):
        form.instance.bien = self.bien
        form.instance.asignado_por = self.request.user
        form.instance.estado = 'pendiente'
        sobrescribir = self.request.POST.get('sobrescribir', '') == '1'
        
        # Busca si ya hay pendiente para ese bien
        asignacion_existente = AsignacionBien.objects.filter(
            bien=self.bien, estado='pendiente'
        ).first()

        if asignacion_existente and not sobrescribir:
            # Hay pendiente y no está confirmado el reemplazo
            messages.warning(self.request,
                f'Ya existe una asignación pendiente para este bien: '
                f'{asignacion_existente.responsable}. ¿Quieres sobrescribirla?'
            )
            # Recarga el form, pero ahora con 'sobrescribir'
            ctx = self.get_context_data(form=form)
            ctx['show_confirm'] = True
            return self.render_to_response(ctx)
        
        # Si sobrescribir, cancelar la anterior
        if asignacion_existente and sobrescribir:
            asignacion_existente.estado = 'cancelado'
            asignacion_existente.save()
            messages.info(self.request, f'La asignación previa fue cancelada y se creó una nueva.')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bien_detalle:desagrupado', kwargs={
            'nombre_bien': self.bien.nombre_bien,
            'categoria_id': self.bien.categoria.id,
            'subcategoria_id': self.bien.subcategoria.id if self.bien.subcategoria else 0,
        })  

class ConfirmarFirmaView(PantallaRequiredMixin, UpdateView):
    model = AsignacionBien
    fields = []
    template_name = 'Asignaciones/confirmar_firma.html'
    pantalla_required = '0021'  # Otro código de permiso

    def get_object(self, queryset=None):
        return get_object_or_404(AsignacionBien, pk=self.kwargs['pk'], estado='pendiente')

    def post(self, request, *args, **kwargs):
        asignacion = self.get_object()
        asignacion.estado = 'firmado'
        asignacion.fecha_firma = timezone.now()
        asignacion.save()
        # Actualiza el responsable del bien
        bien = asignacion.bien
        bien.responsable = asignacion.responsable
        bien.save()
        # Aquí puedes llamar a crear historial también
        return redirect('bien_detalle:desagrupado',
                        nombre_bien=bien.nombre_bien,
                        categoria_id=bien.categoria.id,
                        subcategoria_id=bien.subcategoria.id if bien.subcategoria else 0)

class CancelarAsignacionView(PantallaRequiredMixin, UpdateView):
    model = AsignacionBien
    fields = []
    template_name = 'asignaciones/cancelar.html'
    pantalla_required = '0021'

    def get_object(self, queryset=None):
        return get_object_or_404(AsignacionBien, pk=self.kwargs['pk'], estado='pendiente')

    def post(self, request, *args, **kwargs):
        asignacion = self.get_object()
        asignacion.estado = 'cancelado'
        asignacion.save()
        # Aquí igual puedes llamar a crear historial
        return redirect('bien_detalle:desagrupado',
                        nombre_bien=asignacion.bien.nombre_bien,
                        categoria_id=asignacion.bien.categoria.id,
                        subcategoria_id=asignacion.bien.subcategoria.id if asignacion.bien.subcategoria else 0)

# PDF
def exportar_pendientes_pdf(request, responsable_id):
    MESES_ES = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre",
    }

    recibe = f"{request.GET.get('recibe_cargo_abrev', '')} {request.GET.get('recibe_nombre', '')}"
    recibe_cargo = request.GET.get('recibe_cargo_completo', '')

    firma = f"{request.GET.get('firma_cargo_abrev', '')} {request.GET.get('firma_nombre', '')}"
    firma_cargo = request.GET.get('firma_cargo_completo', '')

    fecha_actual = datetime.now()
    mes_ingles = fecha_actual.strftime("%B")
    mes_espanol = MESES_ES.get(mes_ingles, mes_ingles)

    # Obtén todas las asignaciones pendientes para ese responsable
    asignaciones = AsignacionBien.objects.filter(responsable_id=responsable_id, estado='pendiente').select_related('bien')
    responsable = asignaciones.first().responsable if asignaciones.exists() else None

    # Para mostrar solo el nombre:
    responsable_nombre = ""
    responsable_identidad = ""
    if responsable:
        partes = str(responsable).split("-", 2)
        responsable_nombre = partes[1].strip() if len(partes) > 1 else str(responsable)
        responsable_nombre = responsable_nombre.title()
        responsable_identidad = partes[2].strip() if len(partes) > 2 else str(responsable)

    headers = ["No. Inventario", "Nombre del Bien", "Categoría", "Ubicación"]
    rows = []
    for asignacion in asignaciones:
        bien = asignacion.bien
        rows.append([
            bien.numero_inventario,
            bien.nombre_bien,
            bien.categoria,
            bien.ubicacion,
        ])

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="bienes_pendientes_{responsable}.pdf"'

    c = Canvas(response, pagesize=letter)
    width, height = letter  
    per_page = 10
    page = 1

    logo_path = os.path.join(settings.BASE_DIR, "static/assets/img/logo.png")
    grey_logo = os.path.join(settings.BASE_DIR, "static/assets/img/logo_gris.png")
    bottom_text = os.path.join(settings.BASE_DIR, "static/assets/img/bottom_text.png")

    # Tabla

    for start in range(0, len(rows), per_page):
            table_data = [headers] + rows[start:start+per_page]
            table = Table(table_data, repeatRows=1, colWidths=[80, 150, 150, 120])
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
    
            user = request.user.get_full_name()
            user = user.title()
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString((width ) / 2, height - 165, "COMPROBANTE DE ENTREGA")
            c.setFont("Helvetica", 10)
            c.drawString((width) / 8 , height - 30, f"Usuario: {user}")
            c.drawString(450, height - 30, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

            if responsable:
                c.setFont("Helvetica", 10)
                c.drawString((width) / 8 , height - 45, f"Responsable: {responsable_nombre}")

            c.setFillColor(CMYKColor(0, 0, 0, 1))
            c.setFont("Helvetica", 14)
            c.drawString((width / 8) + 10,(height / 1.3) - 20, f'En fecha {datetime.now().strftime("%d")} de {mes_espanol} del año {datetime.now().strftime("%Y")} se entrega en calidad de préstamo')
            c.drawString((width / 8) + 10,(height / 1.3) - 40, f'a {responsable_nombre} con identidad No. {responsable_identidad} ')
            c.drawString((width / 8) + 10,(height / 1.3) - 60, f'asignado a la Unidad de Financiamiento Transparencia y Fiscalización')
            c.drawString((width / 8) + 10,(height / 1.3) - 80, f'a Partidos Políticos Y Candidatos lo que a continuación se detalla.')
            
            

            w, h = table.wrap(0, 0)
            x = (width - w) / 2
            y = (height - 280) - h
            table.drawOn(c, x, y)

            c.setFillColor(CMYKColor(0, 0, 0, 1))
            c.setFont("Helvetica", 14)
            c.drawString((width / 8),(height / 2) - 115, 'Normativas:')

            c.setFillColor(CMYKColor(0, 0, 0, 1))
            c.setFont("Helvetica", 12)
            c.drawString((width / 6),(height / 2) - 135, '•  Quien recibe se hace responsable de la administración, uso y custodia de los')
            c.drawString((width / 6),(height / 2) - 150, '   bienes antes descritos')

            c.setFillColor(CMYKColor(0, 0, 0, 1))
            c.setFont("Helvetica", 12)
            c.drawString((width / 6),(height / 2) - 165, '•  En caso de extravío el responsable se compromete a reponer el o los mismos ')
            c.drawString((width / 6),(height / 2) - 180, '   en lapso establecido por la Unidad con las características y condiciones iguales')
            c.drawString((width / 6),(height / 2) - 195, '   o similares a las señalas en este comprobante de entrega')
                 

            c.setFillColor(CMYKColor(0, 0, 0, 1))
            c.setFont("Helvetica", 10)
            c.drawString((width / 8) + 10,(height / 5) , '____________________')
            c.drawCentredString((width / 8) + 65,(height / 5) - 18 , f'{user}')
            c.drawCentredString((width / 8) + 65,(height / 5) - 32, 'Encargado(a) de Bienes y')
            c.drawCentredString((width / 8) + 65,(height / 5) - 46, 'Proveeduría')

            

            c.setFillColor(CMYKColor(0, 0, 0, 1))
            c.setFont("Helvetica", 10)
            c.drawString((width / 8) + 170,(height / 5) , '____________________')
            c.drawString((width / 8) + 210,(height / 5) - 18 , 'Recibe:')
            c.drawCentredString((width / 8) + 225,(height / 5) - 32,f"{recibe}")
            c.drawCentredString((width / 8) + 225,(height / 5) - 46,f"{recibe_cargo}")

            c.setFillColor(CMYKColor(0, 0, 0, 1))
            c.setFont("Helvetica", 10)
            c.drawString((width / 2.5) + 170,(height / 5) , '____________________')
            c.drawString((width / 2.5) + 210,(height / 5) - 18 , 'Firma:')
            c.drawCentredString((width / 2.5) + 225,(height / 5) - 32,f"{firma}")
            c.drawCentredString((width / 2.5) + 225,(height / 5) - 46,f"{firma_cargo}")
            


            c.setFont("Helvetica", 9)
            c.setFillColor(colors.white)
            c.drawCentredString(width / 2, 20, f"Página {page}")
            page += 1
            c.showPage()

    
    c.save()
    return response