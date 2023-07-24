from django import forms
from .models import Paciente
from django.forms import DateInput

#-------------------------------------------------------------------------------------------------------#
class PacienteCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dueño'].empty_label = '--- Seleccione una opción ---'
        self.fields['especie'].empty_label = '--- Seleccione una opción ---'
        self.fields['genero'].empty_label = '--- Seleccione una opción ---'

    class Meta:
        model = Paciente
        fields = ['dueño','nombre', 'raza', 'edad', 'fecha_nac', 'nro_chip', 'color', 'especie', 'genero', 'foto','fallecido', 'extraviado', 'activo']
        widgets = {
            'dueño': forms.Select(attrs={'placeholder': 'Seleccione al cliente'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la mascota'}),
            'raza': forms.TextInput(attrs={'placeholder': 'Ingrese la raza de la mascota'}),
            'edad': forms.NumberInput(attrs={'placeholder': 'Ingrese la edad de la mascota'}),
            'fecha_nac': DateInput(attrs={'type': 'date'}),
            'nro_chip': forms.TextInput(attrs={'placeholder': 'Ingrese la Identificación de la mascota'}),
            'foto': forms.ClearableFileInput(),
            'color': forms.TextInput(attrs={'placeholder': 'Ingrese el color de la mascota'}),
            'fallecido': forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
            'extraviado': forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
            'activo': forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
            'especie': forms.Select(attrs={'placeholder': 'Seleccione la especie '}),
            'genero': forms.Select(attrs={'placeholder': 'Seleccione el genero '}),
        }
        labels = {
            'dueño': 'Cliente *',
            'nombre': 'Nombre *',
            'raza': 'Raza (opcional)',
            'edad': 'Edad (opcional)',
            'fecha_nac': 'Fecha de Nacimiento (opcional)',
            'nro_chip': 'Nro. de Chip (opcional)',
            'foto': 'Imagen paciente (opcional)',
            'color': 'Color (opcional)',
            'fallecido': 'Estado fallecido',
            'extraviado': 'Estado extraviado',
            'activo': 'Estado Activo *',
            'especie': 'Especie *',
            'genero': 'Género *',
        }

#-------------------------------------------------------------------------------------------------------#
class PacienteUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dueño'].empty_label = '--- Seleccione una opción ---'
        self.fields['especie'].empty_label = '--- Seleccione una opción ---'
        self.fields['genero'].empty_label = '--- Seleccione una opción ---'

    class Meta:
        model = Paciente
        fields = ['dueño','nombre', 'raza', 'edad', 'fecha_nac', 'nro_chip', 'color', 'especie', 'genero', 'foto','fallecido', 'extraviado', 'activo']
        widgets = {
            'dueño': forms.Select(attrs={'placeholder': 'Seleccione al cliente'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la mascota'}),
            'raza': forms.TextInput(attrs={'placeholder': 'Ingrese la raza de la mascota'}),
            'edad': forms.NumberInput(attrs={'placeholder': 'Ingrese la edad de la mascota'}),
            'fecha_nac': DateInput(attrs={'type': 'date'}),
            'nro_chip': forms.TextInput(attrs={'placeholder': 'Ingrese la Identificación de la mascota'}),
            'foto': forms.ClearableFileInput(),
            'color': forms.TextInput(attrs={'placeholder': 'Ingrese el color de la mascota'}),
            'fallecido': forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
            'extraviado': forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
            'activo': forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
            'especie': forms.Select(attrs={'placeholder': 'Seleccione la especie '}),
            'genero': forms.Select(attrs={'placeholder': 'Seleccione el genero '}),
        }
        labels = {
            'dueño': 'Cliente *',
            'nombre': 'Nombre *',
            'raza': 'Raza (opcional)',
            'edad': 'Edad (opcional)',
            'fecha_nac': 'Fecha de Nacimiento (opcional)',
            'nro_chip': 'Nro. de Chip (opcional)',
            'foto': 'Imagen paciente (opcional)',
            'color': 'Color (opcional)',
            'fallecido': 'Estado fallecido',
            'extraviado': 'Estado extraviado',
            'activo': 'Estado Activo *',
            'especie': 'Especie *',
            'genero': 'Género *',
        }

#-------------------------------------------------------------------------------------------------------#