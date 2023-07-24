from django import forms
# Para las validaciones de los campos de los formularios
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Importe archivo 'models.py'
from .models import ContactoModel, SuscripcionModel


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------#
# Formulario para 'Contacto' -> Pagina principal
class ContactoForm(forms.ModelForm):
    # Expresiones regulares de validacion
    regex_letras_espacios = '^[a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+$'

    # Campos 'INPUTS' del formulario
    nombre = forms.CharField(
        max_length=60, 
        widget=forms.TextInput(attrs={
            'class': 'form-control nombre', 
            'id': 'nombre',
            'name': 'nombre',
            'placeholder': 'Ingrese su nombre',
            }
        ),
        validators=[RegexValidator(regex=regex_letras_espacios)],
        # error_messages={'required': '', 
        #                 'invalid': 'Ingresa tu nombre. Este campo solo puede contener letras.'}
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control correo', 
            'id': 'correo',
            'name': 'correo',
            'placeholder': 'Ingrese su correo electrónico'}
        ),
        # error_messages={'required': '', 
        #                 'invalid': 'Ingresa un correo electrónico válido.'}
    )
    asunto = forms.CharField(
        max_length=60, 
        widget=forms.TextInput(attrs={
            'class': 'form-control asunto',
            'id': 'asunto',
            'name': 'asunto', 
            'placeholder': 'Ingrese el asunto'}
        ),
        # validators=[RegexValidator(regex=regex_letras_espacios)],
        # error_messages={'required': '', 
        #                 'invalid': 'Ingresa el asunto. Este campo solo puede contener letras.'}
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
        'class': 'form-control mensaje', 
        'id': 'mensaje',
        'name': 'mensaje',
        'placeholder': 'Escriba aquí su mensaje',
        'rows': 3}
        ),
        # error_messages={'required': '',
        #                 'invalid': 'Ingresa tu mensaje.'}
    )

    # Clase Meta
    class Meta:
        model = ContactoModel
        fields = ['nombre', 'correo', 'asunto', 'mensaje']





#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------#
# Formulario para 'Suscripcion' -> Pagina principal
class SuscripcionForm(forms.ModelForm):
    email = forms.EmailField(label='Porfavor ingrese un correo válido')
    
    class Meta:
        model = SuscripcionModel
        fields = ['email']
        widgets = {'email': forms.EmailInput(attrs={'placeholder': 'Ingresa tú correo'})}

    def save(self, commit=True):
        # Primero, llama al método save() de la superclase
        subscribe_footer = super().save(commit=False)
        # Luego, haz cualquier cambio que necesites en el objeto suscripcion
        subscribe_footer.email = self.cleaned_data['email']
        # Finalmente, llama al método save() en el objeto suscripcion si commit es True
        if commit:
            subscribe_footer.save()
        return subscribe_footer