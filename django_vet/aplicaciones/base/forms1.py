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
            'class': 'form-control', 
            'id': 'nombre',
            'name': 'nombre',
            'placeholder': 'Ingrese su nombre'}
        ),
        validators=[RegexValidator(regex=regex_letras_espacios)]
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'id': 'correo',
            'name': 'correo',
            'placeholder': 'Ingrese su correo electrónico'}
        )
    )
    asunto = forms.CharField(
        max_length=60, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'asunto',
            'name': 'asunto', 
            'placeholder': 'Ingrese el asunto'}
        ),
        validators=[RegexValidator(regex=regex_letras_espacios)]
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'id': 'mensaje',
        'name': 'mensaje',
        'placeholder': 'Escriba aquí su mensaje', 
        'row': 5}
        )
    )

    # Clase Meta
    class Meta:
        model = ContactoModel
        fields = ['nombre', 'correo', 'asunto', 'mensaje']
   

    # VALIDACION Formulario
    # Campo 'nombre'
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise ValidationError('El campo nombre no puede estar vacío.')
        return nombre
    
    # Campo 'correo'
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo:
            raise ValidationError('El campo correo no puede estar vacío.')

        from django.core.validators import validate_email

        try:
            validate_email(correo)
        except ValidationError:
            raise ValidationError('Ingrese un correo electrónico válido.')
        return correo

    # Campo 'asunto'
    def clean_asunto(self):
        asunto = self.cleaned_data.get('asunto')
        if not asunto:
            raise ValidationError('El campo asunto no puede estar vacío.')
        return asunto

    # Campo 'mensaje'
    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')
        if not mensaje:
            raise ValidationError('El campo mensaje no puede estar vacío.')
        return mensaje


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