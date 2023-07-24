from django.shortcuts import render, redirect
# Importe vista generica TemplateView
from django.views.generic import TemplateView
# Importe archivo 'forms.py'
from .forms import ContactoForm, SuscripcionForm
from django.contrib import messages
# Importe archivo 'models.py'
from .models import SuscripcionModel


#----------------------------------------------------------------------------------------#
# Vista Principal 'index.html' ('urls.py' principal)
class IndexView(TemplateView):
    template_name = 'base/index.html'

#----------------------------------------------------------------------------------------#
# Vista 'servicios' ('urls.py' base)
from django.views.generic import TemplateView
from aplicaciones.servicio.models import Servicio

class ServicioView(TemplateView):
    template_name = 'base/servicios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener la lista de servicios y agregarla al contexto
        context['lista_servicios'] = Servicio.objects.all()
        return context

#----------------------------------------------------------------------------------------#
# Vista 'contacto' ('urls.py' base)
def contactoView(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Guarda la data en la BD
            form.save()

            return redirect('index')
    else:
        form = ContactoForm()

    return render(request, 'base/contacto.html', {'form': form})

#----------------------------------------------------------------------------------------#
# Vista 'suscripcion' del 'footer' ('urls.py' base)
def suscripcionView(request):
    data = {
        'form': SuscripcionForm()
    }
    if request.method == 'POST':
        form = SuscripcionForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not SuscripcionModel.objects.filter(email=email).exists():
                form.save()
                messages.success(request, "Suscrito exitosamente")
            else:
                messages.warning(request, "Ya estás suscrito con este correo electrónico.")
        else:
            messages.error(request, "Hubo un error, No te has suscrito. Ya existe")
            data["form"] = form
    return render(request, 'base/index.html', data)

#------------------------------------------------------------------------------------------------------------#

#Vista de Sección Ayuda
def ayudaView(request):
    return render (request, 'base/ayuda.html')

#------------------------------------------------------------------------------------------------------------#
def empleadoHelpView(request):
    imagenes = [
        {
            'src': 'img/help/empleado/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para crear un empleado, selecciona el menu crear empleado',
        },
        {
            'src': 'img/help/empleado/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/empleado/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Lista los empleados disponibles',
        },
        {
            'src': 'img/help/empleado/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Realiza la busqueda de empleados',
        },
        {
            'src': 'img/help/empleado/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Desabilita a los empleados, modifica o eliminalos del sistema',
        },
    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/empleado_help.html', context)

#------------------------------------------------------------------------------------------------------------#
def clienteHelpView(request):
    imagenes = [
        {
            'src': 'img/help/cliente/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para crear un nuevo cliente, selecciona el menu crear cliente',
        },
        {
            'src': 'img/help/cliente/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/cliente/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Lista los clientes disponibles',
        },
        {
            'src': 'img/help/cliente/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Realiza la busqueda de clientes',
        },
        {
            'src': 'img/help/cliente/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Selecciona entre 2 fechas y crea un informe que puedes ver en pantalla, exportar a pdf o excel',
        },
        {
            'src': 'img/help/cliente/ayuda6.png',
            'alt': 'Imagen 6',
            'texto': 'Modifica o Elimina a los clientes del sistema',
        },
        {
            'src': 'img/help/cliente/ayuda7.png',
            'alt': 'Imagen 7',
            'texto': 'Desabilita a los clientes del sistema',
        },

    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/cliente_help.html', context)
#------------------------------------------------------------------------------------------------------------#
def citaHelpView(request):
    imagenes = [
        {
            'src': 'img/help/cita/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para agendar una cita, debes seleccionar el menú agendar',
        },
        {
            'src': 'img/help/cita/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/cita/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Recibiras un mensaje de exito y una notificación por correo con tú cita',
        },
        {
            'src': 'img/help/cita/ayuda6.png',
            'alt': 'Imagen 6',
            'texto': 'Recibe un correo con la notificación de tu agendamiento',
        },
        {
            'src': 'img/help/cita/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Puedes modificar la cita o eliminarla, si la modificas recibiras una notificación por correo',
        },
        {
            'src': 'img/help/cita/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Puedes buscar tus citas medicas',
        },
        

    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/agendamiento_help.html', context)

#------------------------------------------------------------------------------------------------------------#
def proveedorHelpView(request):
    imagenes = [
        {
            'src': 'img/help/proveedor/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para crear un nuevo proveedor, selecciona el menu crear proveedor',
        },
        {
            'src': 'img/help/proveedor/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/proveedor/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Lista los proveedores disponibles',
        },
        {
            'src': 'img/help/proveedor/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Puedes eliminar o modificar a los proveedores',
        },
        {
            'src': 'img/help/proveedor/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Puedes buscar a un proveedor',
        },
        {
            'src': 'img/help/proveedor/ayuda6.png',
            'alt': 'Imagen 6',
            'texto': 'Modifica o Elimina a los clientes del sistema',
        },
        {
            'src': 'img/help/proveedor/ayuda7.png',
            'alt': 'Imagen 7',
            'texto': 'Desabilita a los clientes del sistema',
        },

    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/proveedor_help.html', context)
#------------------------------------------------------------------------------------------------------------#
def consultaHelpView(request):
    imagenes = [
        {
            'src': 'img/help/consulta/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para registrar una nueva consulta, selecciona el menu crear consulta',
        },
        {
            'src': 'img/help/consulta/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/consulta/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Lista las consultas realizadas',
        },
        {
            'src': 'img/help/consulta/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Modifica o Elimina a los clientes del sistema',
        },
        {
            'src': 'img/help/consulta/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Realiza la busqueda de consultas',
        },
        {
            'src': 'img/help/consulta/ayuda6.png',
            'alt': 'Imagen 6',
            'texto': 'Selecciona ver, para ver el detalle de la consulta',
        },
        {
            'src': 'img/help/consulta/ayuda7.png',
            'alt': 'Imagen 7',
            'texto': 'Aqui puedes ver el detalle de la consulta',
        },
        {
            'src': 'img/help/consulta/ayuda8.png',
            'alt': 'Imagen 8',
            'texto': 'Tienes opciones disponibles de edicion y de exportar a pdf la consulta',
        },
        {
            'src': 'img/help/consulta/ayuda9.png',
            'alt': 'Imagen 9',
            'texto': 'Puedes descargar el pdf de la consulta',
        },
        {
            'src': 'img/help/consulta/ayuda10.png',
            'alt': 'Imagen 10',
            'texto': 'Selecciona entre 2 fechas y crea un informe que puedes ver en pantalla, exportar a pdf o excel',
        },

    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/consultamedica_help.html', context)
#------------------------------------------------------------------------------------------------------------#
def inventarioHelpView(request):
    imagenes = [
        {
            'src': 'img/help/inventario/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para registrar un producto, selecciona el menu crear producto de inventario',
        },
        {
            'src': 'img/help/inventario/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/inventario/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Lista los productos disponibles',
        },
        {
            'src': 'img/help/inventario/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Modifica o Elimina a los productos del sistema',
        },
        {
            'src': 'img/help/inventario/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Realiza la busqueda de productos',
        },
        {
            'src': 'img/help/inventario/ayuda6.png',
            'alt': 'Imagen 6',
            'texto': 'Selecciona la imagen del producto para acceder al detalle',
        },
        {
            'src': 'img/help/inventario/ayuda7.png',
            'alt': 'Imagen 7',
            'texto': 'Puedes ver el detalle del producto',
        },
        {
            'src': 'img/help/inventario/ayuda8.png',
            'alt': 'Imagen 8',
            'texto': 'Selecciona registrar consumo',
        },
        {
            'src': 'img/help/inventario/ayuda9.png',
            'alt': 'Imagen 9',
            'texto': 'Selecciona el producto y la cantidad utilizada, luego guarda',
        },
         {
            'src': 'img/help/inventario/ayuda10.png',
            'alt': 'Imagen 10',
            'texto': 'Si el producto esta bajo el nivel de stock se enviara un correo al administrador detallando el stock del producto.',
        },
        {
            'src': 'img/help/inventario/ayuda11.png',
            'alt': 'Imagen 11',
            'texto': 'Como administrador, revisa tu bandeja de entraga de tu correo.',
        },

    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/inventario_help.html', context)
#------------------------------------------------------------------------------------------------------------#
def servicioHelpView(request):
    imagenes = [
        {
            'src': 'img/help/servicio/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para crear un nuevo servicio, selecciona el menu crear servicio',
        },
        {
            'src': 'img/help/servicio/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/servicio/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Lista los servicios disponibles',
        },
        {
            'src': 'img/help/servicio/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Modifica o Elimina a los clientes del sistema',
        },
        {
            'src': 'img/help/servicio/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Realiza la busqueda de clientes',
        },
    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/servicio_help.html', context)


#------------------------------------------------------------------------------------------------------------#
def pacienteHelpView(request):
    imagenes = [
        {
            'src': 'img/help/paciente/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para crear un nuevo paciente/mascota, selecciona el menu crear paciente',
        },
        {
            'src': 'img/help/paciente/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Luego, Completa el formulario y guarda',
        },
        {
            'src': 'img/help/paciente/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Lista los pacientes/mascotas disponibles',
        },
        {
            'src': 'img/help/paciente/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Puedes modificar o eliminar un paciente o mascota',
        },
        {
            'src': 'img/help/paciente/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Selecciona historial para acceder al historial de la mascota',
        },
        {
            'src': 'img/help/paciente/ayuda8.png',
            'alt': 'Imagen 8',
            'texto': 'Aqui puede visualizar el historial de atenciones del paciente',
        },
        {
            'src': 'img/help/paciente/ayuda6.png',
            'alt': 'Imagen 6',
            'texto': 'Pincha la imagen de la mascota/paciente para acceder a su información',
        },
        {
            'src': 'img/help/paciente/ayuda7.png',
            'alt': 'Imagen 7',
            'texto': 'Aquí puedes ver la información del paciente',
        },

    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/paciente_help.html', context)


#------------------------------------------------------------------------------------------------------------#
def reporteHelpView(request):
    imagenes = [
        {
            'src': 'img/help/reporte/ayuda1.png',
            'alt': 'Imagen 1',
            'texto': 'Para obtener reportes de clientes, selecciona ver clientes',
        },
        {
            'src': 'img/help/reporte/ayuda2.png',
            'alt': 'Imagen 2',
            'texto': 'Selecciona entre 2 fechas y crea un informe que puedes ver en pantalla, exportar a pdf o excel',
        },
        {
            'src': 'img/help/reporte/ayuda3.png',
            'alt': 'Imagen 3',
            'texto': 'Para obtener reportes de pacientes, selecciona ver pacientes',
        },
        {
            'src': 'img/help/reporte/ayuda4.png',
            'alt': 'Imagen 4',
            'texto': 'Selecciona entre 2 fechas y crea un informe que puedes ver en pantalla, exportar a pdf o excel',
        },
        {
            'src': 'img/help/reporte/ayuda5.png',
            'alt': 'Imagen 5',
            'texto': 'Para obtener reportes de consultas, selecciona ver consultas',
        },
        {
            'src': 'img/help/reporte/ayuda6.png',
            'alt': 'Imagen 6',
            'texto': 'Selecciona entre 2 fechas y crea un informe que puedes ver en pantalla, exportar a pdf o excel',
        },

    ]
    context = {
        'imagenes': imagenes,
    }
    return render(request, 'ayuda/reporte_help.html', context)