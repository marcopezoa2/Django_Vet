
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.core import validators
from django.db.models import CheckConstraint, Q
from aplicaciones.paciente.models import Paciente
from datetime import datetime
import re
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
#------------------------------------------------------------------------------------------------------------------------------#
class Region(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
    
    def __str__(self):
        return self.nombre
#------------------------------------------------------------------------------------------------------------------------------#
class Comuna(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
    
    def __str__(self):
        return self.nombre
#------------------------------------------------------------------------------------------------------------------------------# 
# class Especialidad(models.Model):
#     nombre = models.CharField(max_length=50, unique=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

#     class Meta:
#         verbose_name = 'Especialidad'
#         verbose_name_plural = 'Especialidades'
#         ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
    
#     def __str__(self):
#         return self.nombre
# #------------------------------------------------------------------------------------------------------------------------------#
# class Cargo(models.Model):
#     nombre = models.CharField(max_length=50, unique=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

#     class Meta:
#         verbose_name = 'Cargo'
#         verbose_name_plural = 'Cargos'
#         ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
    
#     def __str__(self):
#         return self.nombre
#------------------------------------------------------------------------------------------------------------------------------#
class User(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('veterinario', 'Veterinario'),
        ('recepcionista', 'Recepcionista'),
        ('administrador', 'Administrador'),
]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='cliente')
    username = models.CharField(
        'Nombre de Usuario', max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Proporcione un nombre de usuario válido. '
                'Este valor debe contener solo letras, números y los caracteres: @/./+/-/_.'
                ,  'invalido'
            )
        ], help_text='Un nombre corto que se utilizará para identificarlo de forma única en la plataforma.'
    )
    rut = models.CharField(max_length=12, unique=True,null=True)
    first_name = models.CharField('Nombre', max_length=50,null=True )
    last_name = models.CharField('Apellido', max_length=50, null=True)
    email = models.EmailField('Correo', unique=True,max_length=100,null=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE,null=True, blank=True)
    telefono = models.CharField(max_length=13,null=True, blank=True)
    is_staff = models.BooleanField('Equipo', default=False)
    is_active = models.BooleanField('Activo', default=True)
    # mascota = models.ManyToManyField(Paciente, related_name='dueño_mascota', blank=True)
    date_joined = models.DateTimeField('Fecha creación', auto_now_add=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)



    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_users',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de sus grupos.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_users',
        blank=True,
        help_text='Permisos específicos para esta usuario.'
    )

    @receiver(post_save, sender='auth.User')
    def set_admin_tipo_usuario(sender, instance, created, **kwargs):
        if created and instance.is_superuser:
            instance.tipo_usuario = 'administrador'
            instance.save()

    #Necesario para iniciar sesión
    USERNAME_FIELD = 'rut'
    #Necesario para el registro obligatorio
    REQUIRED_FIELDS = ['username','first_name','last_name','email','direccion','telefono']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_full_direccion(self):
        return f'{self.direccion} {self.comuna}'
    
    def get_cliente_mascota(self):
        return f'{self.rut} - {self.paciente.nombre}'

    # def __str__(self):
    #     return f'{self.rut}'

    def __str__(self):
        if self.tipo_usuario == 'cliente':
            return str(self.rut)
        elif self.tipo_usuario == 'veterinario':
            return self.get_full_name()
        else:
            return str(self.rut)

#------------------------------------------------------------------------------------------------------------------------------#


