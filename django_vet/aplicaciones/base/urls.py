from django.shortcuts import render
from django.urls import path
# Importe archivo principal/base 'views.py'
from .views import contactoView, pacienteHelpView, reporteHelpView, suscripcionView, IndexView, ServicioView, ayudaView,empleadoHelpView,clienteHelpView,inventarioHelpView,servicioHelpView,proveedorHelpView,citaHelpView,consultaHelpView
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.conf.urls import handler404


app_name = 'home'

urlpatterns = [
    # Registro PATH urls principal/base 
    path('', IndexView.as_view(), name = 'index'),
    path('contacto/', contactoView, name = 'contacto'),
    path('suscripcion/',suscripcionView, name= 'suscripcion'),
    path('servicios/',ServicioView.as_view(), name= 'servicios'),


    path('ayuda/',ayudaView, name= 'ayuda'),
    path('ayuda/empleado/',empleadoHelpView, name= 'empleado_help'),
    path('ayuda/cliente/',clienteHelpView, name= 'cliente_help'),
    path('ayuda/paciente/',pacienteHelpView, name= 'paciente_help'),
    path('ayuda/servicio/',servicioHelpView, name= 'servicio_help'),
    path('ayuda/proveedor/',proveedorHelpView, name= 'proveedor_help'),
    path('ayuda/agendamiento/',citaHelpView, name= 'cita_help'),
    path('ayuda/consultamedica/',consultaHelpView, name= 'consulta_help'),
    path('ayuda/inventario/',inventarioHelpView, name= 'inventario_help'),
    path('ayuda/reporte/',reporteHelpView, name= 'reporte_help'),

    
]

#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

