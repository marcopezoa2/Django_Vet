from django.db import models
from django.conf import settings
from django import forms
from datetime import timezone
from aplicaciones.accounts.models import User


# Create your models here.
#------------------------------------------------------------------------------------------------------------------------------#
class Especie(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nombre
#------------------------------------------------------------------------------------------------------------------------------#
class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nombre
#------------------------------------------------------------------------------------------------------------------------------#
class Paciente(models.Model):
    dueño = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paciente_dueño',limit_choices_to={'tipo_usuario': 'cliente'})
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT,related_name='paciente', verbose_name="Especie")                          
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT,related_name='paciente',verbose_name="Género")
    fecha_nac = models.DateField(verbose_name="Fecha de nacimiento",blank=True, null=True)
    nombre = models.CharField(max_length=50,verbose_name="Nombre")
    edad = models.IntegerField(blank=True, null=True,help_text=('Expresado en meses'),verbose_name="Edad mascota")
    raza = models.CharField(max_length=50, blank=True, null=True,help_text=('Especifique la raza del animal'), verbose_name="Raza mascota")
    color = models.CharField(max_length=50, blank=True, null=True,verbose_name="Color")
    nro_chip = models.CharField(verbose_name="N° de Chip",max_length=50, unique=True, blank=True, null=True, help_text='N° Chip único')
    fallecido = models.BooleanField(default=False,help_text=('¿La mascota está fallecida?'))
    extraviado = models.BooleanField(default=False,help_text=('¿La mascota está extraviada?'))
    activo = models.BooleanField(default=True,help_text=('¿La mascota está activa en el sistema?'))
    foto = models.ImageField(upload_to='pacientes/',blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="Fecha creación",auto_now=True, auto_now_add=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    

    def get_mascota_cliente(self):
        return f'{self.nombre} {self.dueño.rut}'

    def __str__(self):
        return self.nombre
#-------------------------------------------------------------------------------------------------------#


