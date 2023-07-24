from django.contrib import admin
from .models import Categoria, Producto, RegistroUsoProducto

# Register your models here.
#------------------------------------------------------------------------------------------------------------------------------#
class CategoriaAdmin(admin.ModelAdmin):
    list_display = [
        id,'nombre','fecha_creacion'
    ]
#------------------------------------------------------------------------------------------------------------------------------#
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        id,'nombre','descripcion','categoria','proveedor','cantidad','stock_minimo','precio_venta','precio_compra','imagen','fecha_creacion'
    ]
#------------------------------------------------------------------------------------------------------------------------------#
class RegistroUsoProductoAdmin(admin.ModelAdmin):
    list_display = [
        id,'producto_utilizado','cantidad_utilizada','fecha_consumo'
    ]
#------------------------------------------------------------------------------------------------------------------------------#
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(RegistroUsoProducto,RegistroUsoProductoAdmin)
