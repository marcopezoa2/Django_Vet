from django import forms
from django.contrib.auth.forms import UserCreationForm

from aplicaciones.accounts.utils import validar_rut
from .models import User
from django.forms import ModelForm, TimeInput
# from .models import Horario
from django.contrib.auth import get_user_model
from PIL import Image
import os
from django.conf import settings


import re
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from django import forms
from django.contrib.auth.models import Group, Permission

User = get_user_model()
#------------------------------------------------------------------------------------------------------------------------------#
'''Horario para Veterinario - Uso exclusivo de Administrador - establece el formato de hora y fecha'''
# class HorarioForm(ModelForm):
#     class Meta:
#         model = Horario
#         fields = ['veterinario', 'dia_de_la_semana', 'hora_inicio', 'hora_fin']
#         widgets = {
#             'hora_inicio': TimeInput(format='%H:%M'),
#             'hora_fin': TimeInput(format='%H:%M')
#         } 
#------------------------------------------------------------------------------------------------------------------------------#
'''Usuario Cliente - Uso exclusivo de Cliente/Administrador - creacion usuario por medio del registro html'''
class UserAdminCreationForm(UserCreationForm):  
    class Meta:
        model = User
        fields = ['rut', 'username', 'first_name', 'last_name', 'email','telefono']
        widgets = {
            
            'rut': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese su RUT en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'first_name': forms.TextInput(attrs={'id': 'first-name-input', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'id': 'last-name-input', 'placeholder': 'Ingrese su apellido '}),
            'username': forms.TextInput(attrs={'id': 'username-input', 'placeholder': 'Ingrese un nombre de usuario'}),
            'email': forms.EmailInput(attrs={'id': 'email-input','placeholder': 'Ingrese su correo electrónico'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono-input','placeholder': 'Ingrese su celular o telefono'}),
        }
        labels = {
            'rut': 'RUT *',
            'first_name': 'Nombre *',
            'last_name': 'Apellido *',
            'username': 'Nombre de Usuario *',
            'email': 'Correo electrónico *',
            'telefono': 'Celular (opcional)',
        }

#------------------------------------------------------------------------------------------------------------------------------#
'''Usuario Administrador - Uso exclusivo de Administrador'''
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['rut','first_name','last_name','username', 'email', 'direccion','comuna','telefono','is_active', 'is_staff']
#------------------------------------------------------------------------------------------------------------------------------#
'''Creacion de Cliente - Uso exclusivo de Administrador/Recepcionista'''
class ClienteCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('rut', 'username', 'first_name', 'last_name', 'email', 'telefono')
        widgets = {
            'rut': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese su RUT en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'first_name': forms.TextInput(attrs={'id': 'first-name-input', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'id': 'last-name-input', 'placeholder': 'Ingrese su apellido '}),
            'username': forms.TextInput(attrs={'id': 'username-input', 'placeholder': 'Ingrese un nombre de usuario'}),
            'email': forms.EmailInput(attrs={'id': 'email-input','placeholder': 'Ingrese su correo electrónico'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono-input','placeholder': 'Ingrese su celular o telefono'}),
        }
        labels = {
            'rut': 'RUT *',
            'first_name': 'Nombre *',
            'last_name': 'Apellido *',
            'username': 'Nombre de Usuario *',
            'email': 'Correo electrónico *',
            'telefono': 'Celular (opcional)',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = 'cliente'
        
        if commit:
            user.save()
        return user
#------------------------------------------------------------------------------------------------------------------------------#
'''Actualizacion de Cliente - Uso exclusivo de Administrador/Recepcionista'''
class ClienteUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].empty_label = '--- Seleccione una opción ---'

    class Meta:
        model = User
        fields = ['rut', 'username', 'first_name', 'last_name', 'email','direccion','comuna','telefono']
        widgets = {
            'rut': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese su RUT en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'first_name': forms.TextInput(attrs={'id': 'first-name-input', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'id': 'last-name-input', 'placeholder': 'Ingrese su apellido '}),
            'username': forms.TextInput(attrs={'id': 'username-input', 'placeholder': 'Ingrese un nombre de usuario'}),
            'email': forms.EmailInput(attrs={'id': 'email-input','placeholder': 'Ingrese su correo electrónico'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono-input','placeholder': 'Ingrese su celular o telefono'}),
            'direccion': forms.TextInput(attrs={'id': 'direccion-input','placeholder': 'Ingrese una dirección'}),
            'comuna': forms.Select(attrs={'placeholder': 'Seleccione su comuna'}),
        }
        labels = {
            'rut': 'RUT *',
            'first_name': 'Nombre *',
            'last_name': 'Apellido *',
            'username': 'Nombre de Usuario *',
            'email': 'Correo electrónico *',
            'telefono': 'Celular (opcional)',
            'direccion': 'Dirección (opcional)',
            'comuna': 'Comuna (opcional)',
        }

#------------------------------------------------------------------------------------------------------------------------------#
'''Creacion de Empleado - Uso exclusivo de Administrador'''
class EmpleadoCreationForm(forms.ModelForm):
    # rut = forms.CharField(max_length=12, validators=[validar_rut], help_text='Ingrese un RUT válido.')
    # rut = forms.CharField(max_length=12, validators=[validar_rut], help_text='Ingrese un RUT válido.', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su RUT en formato xx.xxx.xxx-x'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].empty_label = '--- Seleccione una opción ---'

    # def clean_rut(self):
    #     rut = self.cleaned_data['rut']
    #     rut = rut.replace('.', '').replace('-', '').upper()
    #     if not validar_rut(rut):
    #             raise forms.ValidationError('El RUT ingresado no es válido.')
    #     return rut

    class Meta:
        model = User
        fields = ['tipo_usuario','rut', 'username', 'first_name', 'last_name', 'email','direccion','comuna','telefono']
        widgets = {
            'tipo_usuario': forms.Select(attrs={'placeholder': 'Seleccione un tipo de usuario'}),
            'rut': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese su RUT en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'first_name': forms.TextInput(attrs={'id': 'first-name-input', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'id': 'last-name-input', 'placeholder': 'Ingrese su apellido '}),
            'username': forms.TextInput(attrs={'id': 'username-input', 'placeholder': 'Ingrese un nombre de usuario'}),
            'email': forms.EmailInput(attrs={'id': 'email-input','placeholder': 'Ingrese su correo electrónico'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono-input','placeholder': 'Ingrese su celular o telefono'}),
            'direccion': forms.TextInput(attrs={'id': 'direccion-input','placeholder': 'Ingrese una dirección'}),
            'comuna': forms.Select(attrs={'placeholder': 'Seleccione su comuna'}),
            
        }
        labels = {
            'rut': 'RUT *',
            'first_name': 'Nombre *',
            'last_name': 'Apellido *',
            'username': 'Nombre de Usuario *',
            'email': 'Correo electrónico *',
            'telefono': 'Celular (opcional)',
            'direccion': 'Dirección (opcional)',
            'comuna': 'Comuna (opcional)',
            'tipo_usuario': 'Tipo de Usuario *',
        }

#------------------------------------------------------------------------------------------------------------------------------#
'''Actualizacion de Empleado - Uso exclusivo de Administrador/Empleados'''
class EmpleadoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].empty_label = '--- Seleccione una opción ---'

    class Meta:
        model = User
        fields = ['tipo_usuario','rut', 'username', 'first_name', 'last_name', 'email','direccion','comuna','telefono']
        widgets = {
            'rut': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese su RUT en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'first_name': forms.TextInput(attrs={'id': 'first-name-input', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'id': 'last-name-input', 'placeholder': 'Ingrese su apellido '}),
            'username': forms.TextInput(attrs={'id': 'username-input', 'placeholder': 'Ingrese un nombre de usuario'}),
            'email': forms.EmailInput(attrs={'id': 'email-input','placeholder': 'Ingrese su correo electrónico'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono-input','placeholder': 'Ingrese su celular o telefono'}),
            'direccion': forms.TextInput(attrs={'id': 'direccion-input','placeholder': 'Ingrese una dirección'}),
            'comuna': forms.Select(attrs={'placeholder': 'Seleccione su comuna'}),
            'tipo_usuario': forms.Select(attrs={'placeholder': 'Seleccione un tipo de usuario'}),
        }
        labels = {
            'rut': 'RUT *',
            'first_name': 'Nombre *',
            'last_name': 'Apellido *',
            'username': 'Nombre de Usuario *',
            'email': 'Correo electrónico *',
            'telefono': 'Celular (opcional)',
            'direccion': 'Dirección (opcional)',
            'comuna': 'Comuna (opcional)',
            'tipo_usuario': 'Tipo de Usuario *',
        }

#------------------------------------------------------------------------------------------------------------------------------#
'''Actualizacion de Foto perfil - Uso exclusivo de Usuarios - Redimensiona fotos a 150px x 150px'''
class UserImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(),
        }
        labels = {
            'image': 'Archivo',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        image = self.cleaned_data.get('image')

        if image:
            img = Image.open(image)
            img = img.resize((150, 150))  # Redimensionar la imagen a 150x150

            # Obtener la extensión del archivo original
            file_extension = os.path.splitext(image.name)[1].lower()

            # Generar un nombre único para el archivo
            file_name = f'user_{user.id}{file_extension}'

            # Crear el directorio user_images si no existe
            image_dir = os.path.join(settings.MEDIA_ROOT, 'user_images')
            os.makedirs(image_dir, exist_ok=True)

            # Guardar la imagen en la carpeta de medios
            image_path = os.path.join(image_dir, file_name)
            img.save(image_path)

            # Actualizar el campo de imagen con la ruta del archivo en medios
            user.image = os.path.join('user_images', file_name)

        if commit:
            user.save()

        return user
#------------------------------------------------------------------------------------------------------------------------------#

class UserUpdateForm(forms.ModelForm):
    # is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}), required=False)
    # is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}), required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].empty_label = '--- Seleccione una opción ---'
    
    class Meta:
        model = User
        fields = ['rut', 'first_name', 'last_name', 'username', 'email', 'telefono', 'direccion', 'comuna', 'tipo_usuario', 'is_staff', 'is_active']

        widgets = {
            'rut': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese su RUT en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'first_name': forms.TextInput(attrs={'id': 'first-name-input', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'id': 'last-name-input', 'placeholder': 'Ingrese su apellido '}),
            'username': forms.TextInput(attrs={'id': 'username-input', 'placeholder': 'Ingrese un nombre de usuario'}),
            'email': forms.EmailInput(attrs={'id': 'email-input','placeholder': 'Ingrese su correo electrónico'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono-input','placeholder': 'Ingrese su celular o telefono'}),
            'direccion': forms.TextInput(attrs={'id': 'direccion-input','placeholder': 'Ingrese una dirección'}),
            'comuna': forms.Select(attrs={'placeholder': 'Seleccione su comuna'}),
            'tipo_usuario': forms.Select(attrs={'placeholder': 'Seleccione un tipo de usuario'}),
        }
        labels = {
            'rut': 'RUT *',
            'first_name': 'Nombre *',
            'last_name': 'Apellido *',
            'username': 'Nombre de Usuario *',
            'email': 'Correo electrónico *',
            'telefono': 'Celular (opcional)',
            'direccion': 'Dirección (opcional)',
            'comuna': 'Comuna (opcional)',
            'tipo_usuario': 'Tipo de Usuario *',
            'is_staff': 'Parte del Equipo *',
            'is_active': 'Usuario activo *',
        }

#------------------------------------------------------------------------------------------------------------------------------#

class GroupForm(forms.ModelForm):
    name = forms.CharField(label='Group Name')

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']