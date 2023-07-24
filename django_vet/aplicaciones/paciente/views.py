from aplicaciones.accounts.models import User
from .models import Paciente
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.db.models import Q
from .forms import PacienteCreationForm, PacienteUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user
from django.contrib.auth.mixins import PermissionRequiredMixin


def permission_denied(request):
    messages.error(request, 'No tienes permisos para acceder a esta página.')
    return redirect('accounts:index')

#------------------------------------------------------------------------------------------------------------------------------#
class PacienteDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'paciente/paciente_detail.html'
    context_object_name = 'paciente'
    login_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        paciente = self.get_object()
        user = self.request.user

        if user.tipo_usuario == 'cliente' and paciente.dueño != user:
            # El usuario es un cliente pero intenta acceder a la consulta de otro paciente
            messages.error(request, 'No tienes permisos para acceder a este paciente.')
            return redirect('paciente:lista_paciente')

        return super().dispatch(request, *args, **kwargs)
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Listar pacientes - Uso exclusivo de administrador/veterinario/recepcionista'''

class PacienteListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Paciente
    login_url = 'accounts:login'
    template_name = 'paciente/listar_paciente.html'
    context_object_name = 'paciente'
    paginate_by = 5
    permission_required = 'paciente.ver_paciente'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user

        if user.tipo_usuario == 'cliente':
            # El usuario es un cliente, solo muestra sus propios pacientes
            queryset = super().get_queryset().filter(dueño=user)
        else:
            # El usuario es un veterinario, recepcionista o administrador
            queryset = super().get_queryset()

        return queryset

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Crear pacientes - Uso exclusivo de administrador/recepcionista'''

class PacienteCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Paciente
    login_url = 'accounts:login'
    template_name = 'paciente/registro.html'
    form_class = PacienteCreationForm
    success_url = reverse_lazy('paciente:lista_paciente')
    permission_required = 'paciente.crear_paciente'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        if user.tipo_usuario == 'cliente':
            form.fields['dueño'].queryset = User.objects.filter(id=user.id)

        return form   

    def form_valid(self, form):
        especie = form.cleaned_data['especie']
        genero = form.cleaned_data['genero']
        if not especie:
            messages.error(self.request, 'Por favor, seleccione la especie del paciente.')
            return super().form_invalid(form)
        if not genero:
            messages.error(self.request, 'Por favor, seleccione el género del paciente.')
            return super().form_invalid(form)

        messages.success(self.request, 'El paciente se ha registrado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar al paciente.')
        return super().form_invalid(form)
    

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Actualizar pacientes - Uso exclusivo de administrador/veterinario/recepcionista'''
class PacienteUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Paciente
    login_url = 'accounts:login'
    template_name = 'paciente/registro.html'
    form_class = PacienteUpdateForm
    success_url = reverse_lazy('paciente:lista_paciente')
    permission_required = 'paciente.modificar_paciente'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["dueño"].disabled = True
            form.fields["nombre"].disabled = True
            form.fields["raza"].disabled = True
            form.fields["nro_chip"].disabled = True
            form.fields["especie"].disabled = True
            form.fields["genero"].disabled = True
            form.fields["fallecido"].disabled = True
            form.fields["extraviado"].disabled = True
            form.fields["activo"].disabled = True
        return form
    
    def form_valid(self, form):
        especie = form.cleaned_data['especie']
        genero = form.cleaned_data['genero']
        
        if not especie:
            messages.error(self.request, 'Por favor, seleccione la especie del paciente.')
            return super().form_invalid(form)
        
        if not genero:
            messages.error(self.request, 'Por favor, seleccione el género del paciente.')
            return super().form_invalid(form)

        form.instance.especie_id = especie  # Asignar el valor del campo 'especie'
        form.instance.genero_id = genero # Asignar el valor del campo 'genero'
        
        messages.success(self.request, 'El paciente se ha modificado correctamente.')
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al modificar al paciente.')
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Eliminar pacientes - Uso exclusivo de administrador/veterinario/recepcionista'''
class PacienteDeleteView(DeleteView,PermissionRequiredMixin):
    model = Paciente
    login_url = 'accounts:login'
    template_name = 'paciente/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente:lista_paciente')
    permission_required = 'paciente.eliminar_paciente'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Paciente eliminado con éxito!")
        return reverse_lazy('paciente:lista_paciente')
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion Buscar pacientes - Uso exclusivo de administrador/veterinario'''
def buscar_paciente(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese un término de búsqueda."
        return render(request, 'paciente/listar_paciente.html', {'mensaje': mensaje})
    else:
        # Dividir la consulta en palabras individuales
        palabras_clave = query.split()

        # Crear una lista de condiciones OR para cada palabra clave
        condiciones = [Q(nombre__icontains=palabra) |
                       Q(raza__icontains=palabra) |
                       Q(nro_chip__icontains=palabra) |
                       Q(dueño__first_name__icontains=palabra) |
                       Q(dueño__last_name__icontains=palabra) | 
                       Q(dueño__rut__icontains=palabra) | 
                       Q(genero__nombre__icontains=palabra) for palabra in palabras_clave]

        # Combinar las condiciones con OR utilizando el operador '|'
        query_condicion = condiciones.pop()
        for condicion in condiciones:
            query_condicion |= condicion

        # Aplicar la búsqueda utilizando las condiciones construidas
        resultados = Paciente.objects.filter(query_condicion)

        return render(request, 'paciente/listar_paciente.html', {'object_list': resultados})
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para recargar lista de pacientes - Uso exclusivo de administrador/veterinario/recepcionista'''
def recargar_paciente(request):
    pacientes = Paciente.objects.all()
    return render(request, 'paciente/listar_pacientes.html', {'object_list': pacientes})
#------------------------------------------------------------------------------------------------------------------------------#


def reporte_pacientes(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        pacientes = Paciente.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
        total_pacientes = pacientes.count()

        # renderiza una plantilla HTML con los datos del informe
        return render(request, 'paciente/reporte_pacientes.html', {'pacientes': pacientes, 'total_pacientes': total_pacientes})

    return redirect('paciente:listar_paciente')


#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para generar un PDF a partir del HTML que se muestra en pantalla'''
@require_POST
def generar_pdf(request):
    # Obtén los datos necesarios para el informe de paciente
    fecha_inicio = request.POST.get('fecha_inicio')
    fecha_fin = request.POST.get('fecha_fin')

    pacientes = Paciente.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
    total_pacientes = pacientes.count()

    # Crear el objeto PDF utilizando SimpleDocTemplate con orientación horizontal
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_pacientes.pdf"'
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
    column_widths = [table_width * 0.2, table_width * 0.2, table_width * 0.2, table_width * 0.1, table_width * 0.1,table_width * 0.1]  

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

    # Crear la tabla con los datos de las pacientes
    datos = [['Fecha de Creación', 'Cliente', 'Paciente', 'Edad', 'Genero','Especie']]
    for paciente in pacientes:
        fecha_creacion = paciente.fecha_creacion.strftime('%d/%m/%Y')
        datos.append([
            fecha_creacion,
            paciente.dueño,
            paciente.nombre,
            paciente.edad,
            paciente.genero,
            paciente.especie
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
    content.append(Paragraph('Reporte de Pacientes', estilo_titulo))
    content.append(Paragraph(f'Total de pacientes del rango seleccionado: {total_pacientes}', estilo_subtitulo))
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
'''Funcion que genera un reporte de pacientes medicas en EXCEL - Uso exclusivo del Administrador/Veterinario'''   
def generar_reporte_excel(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Columnas
        columns = ['Fecha de Creación', 'Cliente', 'Paciente', 'Edad', 'Género', 'Especie']

        # Obtener los datos de Pacientes en el rango especificado
        pacientes = Paciente.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin]).values(
            'fecha_creacion',
            'dueño',
            'nombre',
            'edad',
            'genero',
            'especie'
        )

        # Generar el reporte en Excel usando los valores de fecha_inicio y fecha_fin

        # Devolver el informe en Excel como respuesta
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reporte_pacientes.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Paciente Data')

        # Estilo de fuente para el encabezado
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        # Escribir el título
        ws.write_merge(0, 0, 0, len(columns) - 1, 'Reporte de Pacientes', font_style)

        # Escribir el total de pacientes del rango seleccionado
        ws.write_merge(1, 1, 0, len(columns) - 1, f'Total de pacientes nuevos del rango seleccionado: {pacientes.count()}', font_style)

        # Escribir encabezados
        for col_num, column in enumerate(columns):
            ws.write(2, col_num, column, font_style)

        # Estilo de fuente para los datos
        font_style = xlwt.XFStyle()

        # Formato de fecha
        date_format = xlwt.easyxf(num_format_str='DD/MM/YYYY')

        # Escribir los datos en el archivo        
        for row_num, paciente in enumerate(pacientes, start=3):
            fecha_creacion = paciente['fecha_creacion'].strftime('%d/%m/%Y')
            ws.write(row_num, 0, fecha_creacion, date_format)
            ws.write(row_num, 1, paciente['dueño'], font_style)
            ws.write(row_num, 2, paciente['nombre'], font_style)
            ws.write(row_num, 3, paciente['edad'], font_style)
            ws.write(row_num, 4, paciente['genero'], font_style)
            ws.write(row_num, 5, paciente['especie'], font_style)

        # Agregar la fecha y hora de creación al final de la página
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.write(row_num + 1, 0, f"Fecha y hora de creación: {now}", font_style)

        wb.save(response)

        return response