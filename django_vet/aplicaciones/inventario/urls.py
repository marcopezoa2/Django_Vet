from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ConsumoProductoView, ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView,ProductoDetailView
from . import views 

app_name = 'inventario'

urlpatterns = [
     path('detalle/<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
    path('listar/', ProductoListView.as_view(), name='lista_producto'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='actualizar_producto'),
    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('listar/', views.recargar_producto, name='listar_producto'),
    path('consumo-producto/', ConsumoProductoView.as_view(), name='consumo_producto'),

]

#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )