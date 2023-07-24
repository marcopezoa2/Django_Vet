from django.db import models


#----------------------------------------------------------------------------------------#
# Modelo 'Contacto' -> Pagina principal
class ContactoModel(models.Model):
    nombre = models.CharField('Nombre', max_length=60)
    correo = models.EmailField('Correo')
    asunto = models.CharField('Asunto', max_length=60,)
    mensaje = models.TextField('Mensaje')
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateField('Fecha de creacion', auto_now=True, auto_now_add=False)

    class Meta:

        # Admin Django
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente

    def __str__(self):
        return self.nombre


#----------------------------------------------------------------------------------------#
# Modelo 'Suscripcion' del Footer -> Pagina principal
class SuscripcionModel(models.Model):
    email = models.EmailField('Correo', unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    fecha_creacion = models.DateField('Fecha de creacion', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Suscripcion'
        verbose_name_plural = 'Suscripciones'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente

    def __str__(self):
        return self.email

