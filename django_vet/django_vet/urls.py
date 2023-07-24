"""
URL configuration for django_vet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importe archivo principal/base 'views.py'
from aplicaciones.base.views import IndexView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Registro vista principal/base 'index.html'
    path('', IndexView.as_view(), name = 'index'),

    # Registro URLs APPs Proyecto
    path('home/', include('aplicaciones.base.urls', namespace='home')), 
    path('proveedor/', include('aplicaciones.proveedor.urls',namespace='proveedor')),
    path('accounts/', include('aplicaciones.accounts.urls',namespace='accounts')),
    path('paciente/', include('aplicaciones.paciente.urls', namespace='paciente')),
    path('inventario/', include('aplicaciones.inventario.urls', namespace='inventario')),
    path('servicio/', include('aplicaciones.servicio.urls', namespace='servicio')),
    path('agendamiento/', include('aplicaciones.cita.urls', namespace='cita')),
    path('consulta/', include('aplicaciones.consulta.urls', namespace='consulta')),
    path('historial/', include('aplicaciones.historial.urls', namespace='historial')),

]


#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# Ruta para la página "Not Found"
urlpatterns += [
    path('not-found/', views.not_found, name='not_found'),
    # Ruta comodín para capturar todas las demás URLs no encontradas
    path('<path:path>', views.not_found),
]