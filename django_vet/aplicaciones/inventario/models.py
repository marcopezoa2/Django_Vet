from django.db import models
from aplicaciones.proveedor.models import Proveedor
from django.contrib import messages
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase de categorias de producto e insumos veterinarios'''
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha creación')

    def __str__(self):
        return self.nombre
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Productos e Insumos Veterinarios (Inventario)'''
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, related_name='productos')
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    stock_minimo = models.PositiveIntegerField(verbose_name='Stock mínimo', validators=[MinValueValidator(0)], null=True)
    precio_venta = models.IntegerField(verbose_name='Precio venta', validators=[MinValueValidator(0)], null=True)
    precio_compra = models.IntegerField(verbose_name='Precio compra', validators=[MinValueValidator(0)], null=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha creación')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
  
    def __str__(self):
        return self.nombre

    def clean(self):
        if self.cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa.')
        
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase consumo de productos e insumos'''
class RegistroUsoProducto(models.Model):
    producto_utilizado = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto consumido')
    cantidad_utilizada = models.PositiveIntegerField(verbose_name='Cantidad consumida')
    fecha_consumo = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha consumo')

    class Meta:
        verbose_name = 'Consumo producto'
        verbose_name_plural = 'Consumo productos'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
#------------------------------------------------------------------------------------------------------------------------------#


