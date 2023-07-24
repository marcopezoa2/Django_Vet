from django import forms
from datetime import date
from aplicaciones.cita.models import Cita
from .models import ConsultaMedica
from aplicaciones.servicio.models import Servicio

#------------------------------------------------------------------------------------------------------------------------------#
'''Formulario de actualización de datos de la consulta'''
class ConsultaUpdateForm(forms.ModelForm):
    vacuna_nombre = forms.CharField(required=False,max_length=50,label='Nombre vacuna (opcional)', widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la vacuna'}))
    vacuna_fecha = forms.DateField(required=False,label='Fecha vacunación (opcional)',widget= forms.DateInput(attrs={'type': 'date'}))
    desparasitacion_nombre = forms.CharField(required=False,max_length=50,label='Nombre desparasitante (opcional)', widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del desparasitante'}))
    desparasitacion_fecha = forms.DateField(required=False,label='Fecha desparasitación (opcional)',widget= forms.DateInput(attrs={'type': 'date'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].empty_label = '--- Seleccione una opción ---'
        self.fields['horario_consulta'].empty_label = '--- Seleccione una opción ---'
        self.fields['horario_consulta'].queryset = Cita.objects.filter(fecha_cita=date.today()) 

    class Meta:
        model = ConsultaMedica
        fields = ['fecha_consulta', 'servicio', 'horario_consulta', 'peso', 'altura', 'temperatura','vacuna_nombre', 'vacuna_fecha','desparasitacion_nombre','desparasitacion_fecha', 'motivo', 'diagnostico', 'tratamiento', 'observaciones','archivos_paciente']
        widgets = {
    
            'fecha_consulta': forms.DateInput(attrs={'type': 'date'}),
            'horario_consulta': forms.Select(attrs={'placeholder': 'Cita agendada'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Ingrese el peso del paciente en Kilogramos'}),
            'altura': forms.NumberInput(attrs={'placeholder': 'Ingrese la altura del paciente en centimetros'}),
            'temperatura': forms.NumberInput(attrs={'placeholder': 'Ingrese la temperatura del paciente en °C'}),
            'motivo': forms.Textarea(attrs={'placeholder': 'Ingrese el motivo de la consulta médica', 'rows': 4}),
            'diagnostico': forms.Textarea(attrs={'placeholder': 'Ingrese el diagnóstico del paciente', 'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'placeholder': 'Ingrese el tratamiento', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'placeholder': 'Ingrese observaciones', 'rows': 4}),
            'archivos_paciente': forms.ClearableFileInput(),
        }
        labels = {
            'servicio': 'Servicio otorgado *',
            'horario_consulta': 'Cita agendada *',
            'fecha_consulta': 'Fecha de la consulta *',
            'peso': 'Peso (kgs) *',
            'altura': 'Altura (cm) *',
            'temperatura': 'Temperatura (°C) *',
            'vacuna_nombre': 'Nombre vacuna (opcional)',
            'vacuna_fecha': 'Fecha vacunación (opcional)',
            'desparasitacion_nombre': 'Nombre desparasitante (opcional)',
            'desparasitacion_fecha': 'Fecha desparasitación (opcional)',
            'motivo': 'Motivo (opcional)',
            'diagnostico': 'Diagnóstico (opcional)',
            'tratamiento': 'Tratamiento (opcional)',
            'observaciones': 'Observaciones (opcional)',
            'archivos_paciente': 'Cargar examen (opcional)'
        }
  
#------------------------------------------------------------------------------------------------------------------------------#
'''Formulario creacion de Consulta Medica, incluye validacion que trae solo citas del dia en que se genera la consulta'''
# class ConsultaCreationForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['servicio'].empty_label = '--- Seleccione una opción ---'
#         self.fields['horario_consulta'].empty_label = '--- Seleccione una opción ---'
#         self.fields['horario_consulta'].queryset = Cita.objects.filter(fecha_cita=date.today()) 

#     class Meta:
#         model = ConsultaMedica
#         fields = ['fecha_consulta', 'horario_consulta', 'peso', 'altura', 'temperatura', 'motivo', 'diagnostico', 'tratamiento', 'observaciones', 'servicio', 'archivos_paciente']
#         widgets = {
#             'fecha_consulta': forms.DateInput(attrs={'placeholder': 'Fecha de la consulta'}),
#             'horario_consulta': forms.Select(attrs={'placeholder': 'Horario de la consulta'}),
#             'peso': forms.NumberInput(attrs={'placeholder': 'Peso (Kgs)'}),
#             'altura': forms.NumberInput(attrs={'placeholder': 'Altura'}),
#             'temperatura': forms.NumberInput(attrs={'placeholder': 'Temperatura (°C)'}),
#             'motivo': forms.Textarea(attrs={'placeholder': 'Motivo, máximo de 1000 caracteres', 'rows': 4}),
#             'diagnostico': forms.Textarea(attrs={'placeholder': 'Diagnóstico', 'rows': 4}),
#             'tratamiento': forms.Textarea(attrs={'placeholder': 'Tratamiento', 'rows': 4}),
#             'observaciones': forms.Textarea(attrs={'placeholder': 'Observaciones', 'rows': 4}),
#             'servicio': forms.Select(attrs={'placeholder': 'Servicio'}),    
#         }
#         labels = {
#             'servicio': 'Servicio',
#             'horario_consulta': 'Horario Consulta',
#         }
        
#------------------------------------------------------------------------------------------------------------------------------#    

from .models import ConsultaMedica, Vacunacion, Desparasitacion

class ConsultaCreationForm(forms.ModelForm):
    vacuna_nombre = forms.CharField(required=False,max_length=50,label='Nombre vacuna (opcional)', widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la vacuna'}))
    vacuna_fecha = forms.DateField(required=False,label='Fecha vacunación (opcional)',widget= forms.DateInput(attrs={'type': 'date'}))
    desparasitacion_nombre = forms.CharField(required=False,max_length=50,label='Nombre desparasitante (opcional)', widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del desparasitante'}))
    desparasitacion_fecha = forms.DateField(required=False,label='Fecha desparasitación (opcional)',widget= forms.DateInput(attrs={'type': 'date'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].empty_label = '--- Seleccione una opción ---'
        self.fields['horario_consulta'].empty_label = '--- Seleccione una opción ---'
        self.fields['horario_consulta'].queryset = Cita.objects.filter(fecha_cita=date.today()) 

    class Meta:
        model = ConsultaMedica
        fields = ['fecha_consulta', 'servicio', 'horario_consulta', 'peso', 'altura', 'temperatura','vacuna_nombre', 'vacuna_fecha','desparasitacion_nombre','desparasitacion_fecha', 'motivo', 'diagnostico', 'tratamiento', 'observaciones','archivos_paciente']
        widgets = {
    
            'fecha_consulta': forms.DateInput(attrs={'type': 'date'}),
            'horario_consulta': forms.Select(attrs={'placeholder': 'Cita agendada'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Ingrese el peso del paciente en Kilogramos'}),
            'altura': forms.NumberInput(attrs={'placeholder': 'Ingrese la altura del paciente en centimetros'}),
            'temperatura': forms.NumberInput(attrs={'placeholder': 'Ingrese la temperatura del paciente en °C'}),
            'motivo': forms.Textarea(attrs={'placeholder': 'Ingrese el motivo de la consulta médica', 'rows': 4}),
            'diagnostico': forms.Textarea(attrs={'placeholder': 'Ingrese el diagnóstico del paciente', 'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'placeholder': 'Ingrese el tratamiento', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'placeholder': 'Ingrese observaciones', 'rows': 4}),
            'archivos_paciente': forms.ClearableFileInput(),
        }
        labels = {
            'servicio': 'Servicio otorgado *',
            'horario_consulta': 'Cita agendada *',
            'fecha_consulta': 'Fecha de la consulta *',
            'peso': 'Peso (kgs) *',
            'altura': 'Altura (cm) *',
            'temperatura': 'Temperatura (°C) *',
            'vacuna_nombre': 'Nombre vacuna (opcional)',
            'vacuna_fecha': 'Fecha vacunación (opcional)',
            'desparasitacion_nombre': 'Nombre desparasitante (opcional)',
            'desparasitacion_fecha': 'Fecha desparasitación (opcional)',
            'motivo': 'Motivo (opcional)',
            'diagnostico': 'Diagnóstico (opcional)',
            'tratamiento': 'Tratamiento (opcional)',
            'observaciones': 'Observaciones (opcional)',
            'archivos_paciente': 'Cargar examen (opcional)'
        }

