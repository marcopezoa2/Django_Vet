from django.db import models


# Create your models here.
class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    costo = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente

    def __str__(self):
        return self.nombre

