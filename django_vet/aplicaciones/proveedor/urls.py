from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView,ProveedorDetailView
from . import views


app_name = 'proveedor'


urlpatterns = [
    path('detalle/<int:pk>/', ProveedorDetailView.as_view(), name='proveedor_detail'),
    path('listar/', ProveedorListView.as_view(), name='lista_proveedor'),
    path('crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('editar/<int:pk>/', ProveedorUpdateView.as_view(), name='actualizar_proveedor'),
    path('eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),
    path('buscar/', views.buscar_proveedor, name='buscar_proveedor'),
    path('listar/', views.recargar_proveedor, name='listar_proveedor'),
]



#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )