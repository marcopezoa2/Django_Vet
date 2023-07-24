from django import forms
from .models import Servicio

#------------------------------------------------------------------------------------------------------------------------------#
class ServicioUpdateForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'costo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del servicio'}),
            'costo': forms.NumberInput(attrs={'placeholder': 'Precio del servicio'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Agregue una descripción del servicio ofrecido', 'rows': 4}),
        }
        labels = {
            'nombre': 'Nombre *',
            'costo': 'Precio *',
            'descripcion': 'Descripción *',
        }
#------------------------------------------------------------------------------------------------------------------------------#
class ServicioCreationForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'costo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del servicio'}),
            'costo': forms.NumberInput(attrs={'placeholder': 'Precio del servicio'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Agregue una descripción del servicio ofrecido', 'rows': 4}),
        }
        labels = {
            'nombre': 'Nombre *',
            'costo': 'Precio *',
            'descripcion': 'Descripción *',
        }
#------------------------------------------------------------------------------------------------------------------------------#