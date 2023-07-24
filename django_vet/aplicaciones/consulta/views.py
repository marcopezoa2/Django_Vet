from datetime import date
from aplicaciones.cita.models import Cita
from aplicaciones.consulta.forms import ConsultaCreationForm, ConsultaUpdateForm
from .models import ConsultaMedica, validate_file_size, Vacunacion, Desparasitacion
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import ValidationError
from django.conf import settings
import os

#----------------------------------------------------------------------------------------#
'''Importaciones para generar un PDF'''
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from datetime import datetime
import io
from django.contrib.auth.mixins import PermissionRequiredMixin

#----------------------------------------------------------------------------------------#
'''Importaciones para generar otro PDF'''
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.decorators.http import require_POST
#----------------------------------------------------------------------------------------#
'''Importaciones para generar reporte en excel'''
import xlwt
#------------------------------------------------------------------------------------------------------------------------------#
from django.db import connection

def permission_denied(request):
    messages.error(request, 'No tienes permisos para acceder a esta página.')
    return redirect('accounts:index')

#------------------------------------------------------------------------------------------------------------------------------#
'''Muestra el detalle de la consulta medica - Uso exclusivo del Administrador/Cliente/Veterinario'''
class ConsultaDetailView(LoginRequiredMixin, DetailView):
    model = ConsultaMedica
    template_name = 'consulta/consulta_detail.html'
    context_object_name = 'consulta'
    login_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        consulta = self.get_object()
        user = self.request.user

        if user.tipo_usuario == 'cliente' and consulta.paciente.dueño != user:
            # El usuario es un cliente pero intenta acceder a la consulta de otro paciente
            messages.error(request, 'No tienes permisos para acceder a esta consulta.')
            return redirect('paciente:lista_paciente')

        return super().dispatch(request, *args, **kwargs)
    

    # def get_queryset(self):
    #     user = self.request.user

    #     if user.tipo_usuario == 'cliente':
    #         # El usuario es un cliente, solo muestra sus propias consultas asociadas a sus pacientes
    #         queryset = super().get_queryset().filter(paciente__dueño=user)
    #     else:
    #         # El usuario es un veterinario, recepcionista o administrador
    #         queryset = super().get_queryset()

    #     return queryset

    
#------------------------------------------------------------------------------------------------------------------------------#
'''Lista las consultas medicas - Uso exclusivo del Administrador/Cliente/Veterinario'''
class ConsultaListView(LoginRequiredMixin,ListView,PermissionRequiredMixin):
    model = ConsultaMedica
    login_url = 'accounts:login'
    template_name = 'consulta/listar_consulta.html'
    context_object_name = 'consulta'
    paginate_by = 10
    permission_required = 'consulta.ver_consulta'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
#------------------------------------------------------------------------------------------------------------------------------#
'''Crea la consulta medica - Uso exclusivo del Administrador/Veterinario'''
class ConsultaCreateView(LoginRequiredMixin, CreateView,PermissionRequiredMixin):
    model = ConsultaMedica
    login_url = 'accounts:login'
    template_name = 'consulta/registro.html'
    form_class = ConsultaCreationForm
    success_url = reverse_lazy('consulta:lista_consulta')
    permission_required = 'consulta.crear_consulta'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
        

    def form_valid(self, form):
        form.instance.user = self.request.user
        archivos_paciente = self.request.FILES.getlist('archivos_paciente')

        for archivo in archivos_paciente:
            try:
                validate_file_size(archivo)
            except ValidationError as e:
                form.add_error('archivos_paciente', e)
                return self.form_invalid(form)

        response = super().form_valid(form)

        # Llamar a la función calcular_imc en la instancia de la ConsultaMedica
        self.object.calcular_imc()
        messages.success(self.request, 'La consulta médica se ha registrado correctamente.')

        # Obtener los datos de vacunación y desparasitación del formulario
        vacuna_nombre = form.cleaned_data.get('vacuna_nombre')
        vacuna_fecha = form.cleaned_data.get('vacuna_fecha')
        desparasitacion_nombre = form.cleaned_data.get('desparasitacion_nombre')
        desparasitacion_fecha = form.cleaned_data.get('desparasitacion_fecha')

        # Guardar los datos de vacunación y desparasitación en la instancia de la ConsultaMedica
        Vacunacion.objects.create(consulta=self.object, nombre=vacuna_nombre, fecha=vacuna_fecha)
        Desparasitacion.objects.create(consulta=self.object, nombre=desparasitacion_nombre, fecha=desparasitacion_fecha)

        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar la consulta.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#
'''Permite descargar un archivo publicado como un examen por ejemplo - Uso exclusivo del Administrador/Veterinario/Cliente'''
def descargar_archivo(request, pk):
    consulta = get_object_or_404(ConsultaMedica, pk=pk)
    archivo = consulta.archivos_paciente
    file_path = archivo.path if os.path.isabs(archivo.name) else os.path.join(settings.MEDIA_ROOT, archivo.name)

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
#------------------------------------------------------------------------------------------------------------------------------#
'''Actualiza los datos de la consulta medica - Uso exclusivo del Administrador/Veterinario'''      
class ConsultaUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin):
    model = ConsultaMedica
    login_url = 'accounts:login'
    template_name = 'consulta/registro.html'
    form_class = ConsultaUpdateForm
    success_url = reverse_lazy('consulta:lista_consulta')
    permission_required = 'consulta.modificar_consulta'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["tratamiento"].disabled = True
        return form

    def form_valid(self, form):
        # Llamar a la función calcular_imc en la instancia de la ConsultaMedica
        self.object.calcular_imc()
        messages.success(self.request, 'La consulta médica se ha modificado correctamente.')
        form.save()
        # return redirect(self.success_url)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al modificar la consulta.')
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------#
'''Elimina una consulta medica - Uso exclusivo del Administrador/Veterinario'''
class ConsultaDeleteView(DeleteView,PermissionRequiredMixin):
    model = ConsultaMedica
    login_url = 'accounts:login'
    template_name = 'consulta/consulta_confirm_delete.html'
    success_url = reverse_lazy('consulta:lista_consulta')
    permission_required = 'consulta.eliminar_consulta'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "¡Consulta eliminada con éxito!")
        return reverse_lazy('consulta:lista_consulta')
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para buscar consultas - Uso exclusivo del Administrador/Recepcionista/Veterinario'''
def buscar_consulta(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese un término de búsqueda."
        return render(request, 'consulta/listar_consulta.html', {'mensaje': mensaje})
    
    else:
        resultados = ConsultaMedica.objects.filter(Q(fecha_consulta__icontains=query))
        return render(request, 'consulta/listar_consulta.html', {'object_list': resultados})

#------------------------------------------------------------------------------------------------------------------------------#
'''Recarga la lista de consultas agendadas - Uso exclusivo del Administrador/Recepcionista/Veterinario'''
def recargar_consulta(request):
    consultas = ConsultaMedica.objects.all()
    return render(request, 'consulta/listar_consulta.html', {'object_list': consultas})

#------------------------------------------------------------------------------------------------------------------------------#
'''Genera un reporte PDF asosiada a una consulta y paciente ID - Uso exclusivo del Administrador/Veterinario'''
def generar_reporte_pdf(request, pk):
    consulta = get_object_or_404(ConsultaMedica, pk=pk)
    buffer = io.BytesIO()

    # Crear el objeto de respuesta HTTP como un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;  filename*=UTF-8\'\'reporte.pdf'

    p = canvas.Canvas(buffer)

    # Crear el objeto PDF utilizando SimpleDocTemplate
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Definir estilos de texto
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Title']
    estilo_titulo.alignment = 1
    estilo_titulo.fontName = 'Helvetica-Bold'
    estilo_parrafo = styles['BodyText']
    estilo_parrafo.fontName = 'Helvetica'
    estilo_texto_celda = ParagraphStyle(
        'TextoCelda',
        parent=estilo_parrafo,
        alignment=0,  # Justificación: 0=izquierda, 1=centro, 2=derecha, 4=justificado
    )

    # Calcular el ancho de la página
    page_width, page_height = letter
    table_width = page_width - (2 * inch)  # Margen izquierdo y derecho de 1 pulgada
    # Calcular el ancho proporcional para cada columna
    column_widths = [table_width * 0.4, table_width * 0.6]  # Ejemplo de distribución 40% - 60%

    # Agregar tabla de estilos
    tabla_estilo = TableStyle([
        ('WORDWRAP', (0, 0), (-1, -1), 'ON'),  # Permite el flujo de texto dentro de las celdas
        ('ROWHEIGHT', (0, 0), (-1, -1), 12),  # Establece el alto de las filas en 12 unidades
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crear elementos para el contenido del PDF
    elementos = []

    # Agregar título
    titulo = Paragraph("Reporte de Consulta Médica", estilo_titulo)
    elementos.append(titulo)

    # Agregar imagen de fondo
    c = canvas.Canvas(response, pagesize=letter)

    logo_path = 'static/img/banner/banner1.jpg'
    logo_width, logo_height = 6.5 * inch, 1.5 * inch

    # Agregar imagen de fondo
    logo = Image(logo_path, width=logo_width, height=logo_height)

    # Obtener las dimensiones de la página
    page_width, page_height = letter

    # Coordenadas para ubicar el logo en la esquina superior derecha
    logo_x = page_width - logo_width - inch  # Margen derecho de 1 pulgada
    logo_y = page_height - logo_height - inch  # Margen superior de 1 pulgada

    # Agregar el logo a la esquina superior derecha
    logo.drawOn(c, logo_x, logo_y)

    # Agregar imagen de fondo
    elementos.append(logo)

    # Agregar tabla de datos
    datos = [
        ['Fecha de Consulta', consulta.fecha_consulta],
        ['Horario de Consulta', consulta.horario_consulta],  # Formatear como hora:minuto
        ['Peso', str(consulta.peso) + ' kg'],  # Convertir a cadena y agregar unidad de medida
        ['Temperatura', str(consulta.temperatura) + ' °C'],  # Convertir a cadena y agregar unidad de medida
        ['Motivo', consulta.motivo],
        ['Diagnóstico', consulta.diagnostico],
        ['Tratamiento', consulta.tratamiento],
        ['Observaciones', consulta.observaciones],
        ['Veterinario', consulta.veterinario.first_name],
        ['Paciente', consulta.paciente.nombre],
        ['Servicio', consulta.servicio.nombre],
    ]

    # Aplicar el estilo de justificación de texto a todas las celdas de texto
    for i in range(1, len(datos)):
        for j in range(len(datos[i])):
            if isinstance(datos[i][j], float):
                datos[i][j] = Paragraph('{:.2f}'.format(datos[i][j]), estilo_texto_celda)  # Formatear como número con 2 decimales
            else:
                datos[i][j] = Paragraph(str(datos[i][j]), estilo_texto_celda)

    tabla = Table(datos, style=tabla_estilo, colWidths=column_widths)
    elementos.append(tabla)

    # Agregar fecha y hora de creación al final de la página
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_creacion = Paragraph(f"Fecha y hora de creación: {now}", estilo_parrafo)
    elementos.append(fecha_creacion)

    # Agregar elementos al documento PDF
    doc.build(elementos)
    p.save()
    
    return response
#--------------------------------------------------#
'''Funcion para generar un PDF a partir del HTML que se muestra en pantalla'''
@require_POST
def generar_pdf(request):
    # Obtén los datos necesarios para el informe de consulta
    fecha_inicio = request.POST.get('fecha_inicio')
    fecha_fin = request.POST.get('fecha_fin')

    consultas = ConsultaMedica.objects.filter(fecha_consulta__range=[fecha_inicio, fecha_fin])
    total_consultas = consultas.count()

    # Crear el objeto PDF utilizando SimpleDocTemplate con orientación horizontal
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_consulta.pdf"'
    result_pdf = BytesIO()
    doc = SimpleDocTemplate(result_pdf, pagesize=landscape(letter))

    # Definir estilos de texto
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Title']
    estilo_titulo.alignment = 1
    estilo_titulo.fontName = 'Helvetica-Bold'
    estilo_parrafo = styles['BodyText']
    estilo_parrafo.fontName = 'Helvetica'
    estilo_parrafo.alignment = 4  # Justificación: 0=izquierda, 1=centro, 2=derecha, 4=justificado
    estilo_parrafo.spaceAfter = 12  # Espacio después del párrafo
    estilo_texto_celda = ParagraphStyle(
        'TextoCelda',
        parent=estilo_parrafo,
        alignment=4,  # Justificación: 0=izquierda, 1=centro, 2=derecha, 4=justificado
    )
    estilo_subtitulo = styles['BodyText']
    estilo_subtitulo.fontName = 'Helvetica-Bold'
    estilo_subtitulo.fontSize = 10
    estilo_subtitulo.alignment = 0  # Justificación: 0=izquierda, 1=centro, 2=derecha, 4=justificado
    
    # Calcular el ancho de la página
    page_width, page_height = landscape(letter)
    table_width = page_width - (2 * inch)  # Margen izquierdo y derecho de 1 pulgada
    # Calcular el ancho proporcional para cada columna
    column_widths = [table_width * 0.15, table_width * 0.15, table_width * 0.2, table_width * 0.25, table_width * 0.25]  

    # Definir el estilo de la tabla
    tabla_estilo = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), 'ON'),  # Permite el flujo de texto dentro de las celdas
        ('ROWHEIGHT', (0, 0), (-1, -1), 12),  # Establece el alto de las filas en 12 unidades
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),#varible de tamaño letra titular tabla
        ('BOTTOMPADDING', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crear la tabla con los datos de las consultas
    datos = [['Fecha de Consulta', 'Veterinario', 'Paciente', 'Diagnóstico', 'Tratamiento']]
    for consulta in consultas:
        datos.append([
            consulta.fecha_consulta,
            consulta.veterinario,
            consulta.paciente,
            consulta.diagnostico,
            consulta.tratamiento
        ])

    # Aplicar el estilo de justificación de texto a todas las celdas de texto
    for i in range(1, len(datos)):
        for j in range(len(datos[i])):
            if isinstance(datos[i][j], float):
                datos[i][j] = Paragraph('{:.2f}'.format(datos[i][j]), estilo_texto_celda)  # Formatear como número con 2 decimales
            else:
                datos[i][j] = Paragraph(str(datos[i][j]), estilo_texto_celda)

    table = Table(datos, colWidths=column_widths)
    table.setStyle(tabla_estilo)  # Aplicar los estilos de la tabla definidos anteriormente

    # Construir el contenido del PDF
    content = []
    content.append(Paragraph('Reporte de Consultas', estilo_titulo))
    content.append(Paragraph(f'Total de consultas del rango seleccionado: {total_consultas}', estilo_subtitulo))
    content.append(table)

    # Agregar fecha y hora de creación al final de la página
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_creacion = Paragraph(f"Fecha y hora de creación: {now}", estilo_parrafo)
    content.append(fecha_creacion)

    # Construir el PDF y escribirlo en la respuesta
    doc.build(content)
    response.write(result_pdf.getvalue())

    return response

#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion que genera un reporte de consultas medicas - Uso exclusivo del Administrador/Veterinario'''
def reporte_consultas(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        consultas = ConsultaMedica.objects.filter(fecha_consulta__range=[fecha_inicio, fecha_fin])
        total_consultas = consultas.count()

        return render(request, 'consulta/reporte_consultas.html', {'consultas': consultas, 'total_consultas': total_consultas})

    return redirect('consulta:listar_consulta')
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion que genera un reporte de consultas medicas en EXCEL - Uso exclusivo del Administrador/Veterinario'''
def generar_reporte_excel(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Columnas
        columns = ['Fecha de Consulta', 'Veterinario', 'Paciente', 'Diagnóstico', 'Tratamiento']

        # Obtener los datos de Consulta en el rango especificado
        consultas = ConsultaMedica.objects.filter(fecha_consulta__range=[fecha_inicio, fecha_fin]).values(
            'fecha_consulta',
            'veterinario__rut',
            'paciente__nombre',
            'diagnostico',
            'tratamiento'
        )

        # Generar el reporte en Excel usando los valores de fecha_inicio y fecha_fin

        # Devolver el informe en Excel como respuesta
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reporte_consulta.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Consulta Data')

        # Estilo de fuente para el encabezado
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        # Escribir el título
        ws.write_merge(0, 0, 0, len(columns) - 1, 'Reporte de Consulas Médicas', font_style)

        # Escribir el total de consults del rango seleccionado
        ws.write_merge(1, 1, 0, len(columns) - 1, f'Total de consultas del rango seleccionado: {consultas.count()}', font_style)

        # Escribir encabezados
        for col_num, column in enumerate(columns):
            ws.write(2, col_num, column, font_style)

        # Estilo de fuente para los datos
        font_style = xlwt.XFStyle()

        # Formato de fecha
        date_format = xlwt.easyxf(num_format_str='DD/MM/YYYY')

        # Escribir los datos en el archivo        
        for row_num, consulta in enumerate(consultas, start=3):
            fecha_consulta = consulta['fecha_consulta'].strftime('%d/%m/%Y')
            ws.write(row_num, 0, fecha_consulta, date_format)
            ws.write(row_num, 1, consulta['veterinario__rut'], font_style)
            ws.write(row_num, 2, consulta['paciente__nombre'], font_style)
            ws.write(row_num, 3, consulta['diagnostico'], font_style)
            ws.write(row_num, 4, consulta['tratamiento'], font_style)

        # Agregar la fecha y hora de creación al final de la página
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.write(row_num + 1, 0, f"Fecha y hora de creación: {now}", font_style)

        wb.save(response)

        return response