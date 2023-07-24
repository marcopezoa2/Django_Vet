from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView,PacienteDetailView, reporte_pacientes,generar_pdf,generar_reporte_excel
from . import views 

app_name = 'aplicaciones.paciente'


urlpatterns = [
    path('detalle/<int:pk>/', PacienteDetailView.as_view(), name='paciente_detail'),
    path('listar/', PacienteListView.as_view(), name='lista_paciente'),
    path('crear/', PacienteCreateView.as_view(), name='crear_paciente'),
    path('editar/<int:pk>/', PacienteUpdateView.as_view(), name='actualizar_paciente'),
    path('eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='eliminar_paciente'),
    path('buscar/', views.buscar_paciente, name='buscar_paciente'),
    path('listar/', views.recargar_paciente, name='listar_paciente'),


    path('reporte/', reporte_pacientes, name='reporte_pacientes'),

    # path('reporte-pdf/<int:pk>', generar_reporte_pdf, name='generar_reporte_pdf'),
    path('generar_pdf', generar_pdf, name='generar_pdf'),
    path('reporte/excel/', generar_reporte_excel, name='generar_reporte_excel'),
]


#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )