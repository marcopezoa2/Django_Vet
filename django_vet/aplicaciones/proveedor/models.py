from django.db import models
from aplicaciones.accounts.models import Comuna

# Create your models here.

#Creacion modelo Provedores
class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100, unique=True)
    rut_empresa = models.CharField(max_length=12, unique=True)
    nombre_contacto = models.CharField(max_length=100, null=True)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True,blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE,related_name='proveedor',blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
    
    def __str__(self):
        return self.nombre_empresa

