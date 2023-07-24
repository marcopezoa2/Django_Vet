from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ConsultaListView, ConsultaCreateView, ConsultaUpdateView, ConsultaDeleteView, ConsultaDetailView, descargar_archivo, generar_reporte_pdf,reporte_consultas,generar_pdf,generar_reporte_excel
from .import views 

app_name = 'consulta'


urlpatterns = [
    path('detalle/<int:pk>/', ConsultaDetailView.as_view(), name='consulta_detail'),
    path('listar/', ConsultaListView.as_view(), name='lista_consulta'),
    path('crear/', ConsultaCreateView.as_view(), name='crear_consulta'),
    path('editar/<int:pk>/', ConsultaUpdateView.as_view(), name='actualizar_consulta'),
    path('eliminar/<int:pk>/', ConsultaDeleteView.as_view(), name='eliminar_consulta'),
    path('buscar/', views.buscar_consulta, name='buscar_consulta'),
    path('listar/', views.recargar_consulta, name='listar_consulta'),

    # path('get-paciente-data/', views.get_paciente_data, name='get_paciente_data'),

    path('descargar_archivo/<int:pk>/', descargar_archivo, name='descargar_archivo'),
    path('reporte-pdf/<int:pk>', generar_reporte_pdf, name='generar_reporte_pdf'),
    # path('reporte/', views.generar_reporte_pdf_reporte_consulta, name='generar_reporte_pdf_reporte_consulta'),


    path('generar_pdf', generar_pdf, name='generar_pdf'),

    path('reporte/', reporte_consultas, name='reporte_consultas'),
    path('reporte/excel/', generar_reporte_excel, name='generar_reporte_excel'),
]

#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

