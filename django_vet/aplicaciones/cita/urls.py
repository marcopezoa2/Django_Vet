from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CitaListView, CitaCreateView, CitaUpdateView, CitaDeleteView
from . import views 

app_name = 'cita'


urlpatterns = [
    path('listar/', CitaListView.as_view(), name='lista_cita'),
    path('crear/', CitaCreateView.as_view(), name='crear_cita'),
    path('editar/<int:pk>/', CitaUpdateView.as_view(), name='actualizar_cita'),
    path('eliminar/<int:pk>/', CitaDeleteView.as_view(), name='eliminar_cita'),
    path('buscar/', views.buscar_cita, name='buscar_cita'),
    path('listar/', views.recargar_cita, name='listar_cita'),
]



#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )