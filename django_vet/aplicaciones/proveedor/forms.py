from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Proveedor

#------------------------------------------------------------------------------------------------------------------------------#
class ProveedorCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].empty_label = '--- Seleccione una opción ---'
        
    class Meta:
        model = Proveedor
        fields = ['rut_empresa', 'nombre_empresa', 'nombre_contacto', 'correo', 'telefono', 'direccion', 'comuna']
        widgets = {
    
            'rut_empresa': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese el RUT de la empresa en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'nombre_empresa': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la empresa'}),
            'nombre_contacto': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre y apellido del contacto'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Ingrese un correo de contacto'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese un telefono de contacto'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'comuna': forms.Select(attrs={'placeholder': 'Seleccione una comuna'}), 
        }
        labels = {
            'nombre_empresa' : 'Nombre empresa *',
            'rut_empresa': 'RUT empresa *',
            'nombre_contacto':  'Nombre contacto *',
            'correo':  'Correo electrónico *',
            'telefono':  'Teléfono (opcional)',
            'direccion':'Dirección (opcional)',
            'comuna': 'Comuna (opcional)',
        }

#------------------------------------------------------------------------------------------------------------------------------#
class ProveedorUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].empty_label = '--- Seleccione una opción ---'

    class Meta:
        model = Proveedor
        fields = ['rut_empresa', 'nombre_empresa', 'nombre_contacto', 'correo', 'telefono', 'direccion', 'comuna']
        widgets = {
            'rut_empresa': forms.TextInput(attrs={'id': 'rutInput', 'placeholder': 'Ingrese el RUT de la empresa en formato xx.xxx.xxx-x', 'oninput': 'formatRutInput()'}),
            'nombre_empresa': forms.TextInput(attrs={ 'placeholder': 'Ingrese el nombre de la empresa'}),
            'nombre_contacto': forms.TextInput(attrs={ 'placeholder': 'Ingrese el nombre y apellido del contacto'}),
            'correo': forms.EmailInput(attrs={'id': 'email-input', 'placeholder': 'Ingrese un correo de contacto'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono-input', 'placeholder': 'Ingrese un telefono de contacto'}),
            'direccion': forms.TextInput(attrs={'id': 'direccion-input', 'placeholder': 'Ingrese una dirección'}),
            'comuna': forms.Select(attrs={'placeholder': 'Seleccione una comuna'}),    
        }
        labels = {
            'nombre_empresa' : 'Nombre empresa *',
            'rut_empresa': 'RUT empresa *',
            'nombre_contacto':  'Nombre contacto *',
            'correo':  'Correo electrónico *',
            'telefono':  'Teléfono (opcional)',
            'direccion':'Dirección (opcional)',
            'comuna': 'Comuna (opcional)',
        }

#------------------------------------------------------------------------------------------------------------------------------#