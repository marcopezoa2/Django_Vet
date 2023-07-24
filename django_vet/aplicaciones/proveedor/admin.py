from django.contrib import admin
# Importe archivo 'models.py'
from .models import Proveedor

# Register your models here.

class ProveedorAdmin(admin.ModelAdmin):
    list_display = [
        id,'nombre_empresa', 'rut_empresa','nombre_contacto', 'correo', 'telefono', 'direccion', 'comuna','fecha_creacion'
    ]

admin.site.register(Proveedor,ProveedorAdmin)
