from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ServicioListView, ServicioCreateView, ServicioUpdateView, ServicioDeleteView
from . import views 

app_name = 'servicio'


urlpatterns = [
    path('listar/', ServicioListView.as_view(), name='lista_servicio'),
    path('crear/', ServicioCreateView.as_view(), name='crear_servicio'),
    path('editar/<int:pk>/', ServicioUpdateView.as_view(), name='actualizar_servicio'),
    path('eliminar/<int:pk>/', ServicioDeleteView.as_view(), name='eliminar_servicio'),
    path('buscar/', views.buscar_servicio, name='buscar_servicio'),
    path('listar/', views.recargar_servicio, name='listar_servicio'),

    path('publicar-servicio/',  views.publicar_servicio, name='publicar_servicio'),
]



#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )