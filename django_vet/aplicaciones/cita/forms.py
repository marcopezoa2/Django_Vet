from django import forms
from django.forms import ModelForm
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from .models import Cita
from django.forms import DateInput


#---------------------------------------------------------------------------------#
class CitaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['fecha_cita'].empty_label = '--- Seleccione una opción ---'
        self.fields['veterinario'].empty_label = '--- Seleccione una opción ---'
        self.fields['paciente'].empty_label = '--- Seleccione una opción ---'
        # Eliminar la primera opción del campo horario si comienza con "---------"
        first_option = self.fields['horario'].choices[0]
        if isinstance(first_option, (list, tuple)) and len(first_option) == 2 and first_option[1].startswith('---------'):
            self.fields['horario'].choices = self.fields['horario'].choices[1:]

        # Agregar la opción "Seleccione una opción" al principio
        self.fields['horario'].choices.insert(0, ('', '--- Seleccione una opción ---'))

    class Meta:
        model = Cita
        fields = ['fecha_cita', 'veterinario', 'paciente', 'horario']
        widgets = {
            'fecha_cita': DateInput(attrs={'type': 'date'})
        }
        labels = {
            'fecha_cita': 'Fecha de atención *',
            'veterinario': 'Veterinario  *',
            'paciente': 'Paciente o Mascota *',
            'horario': 'Horario de atención *',
        }

    def get_horario_display(self):
        horario = self.cleaned_data.get('horario')
        for option in Cita.HORARIOS:
            if option[0] == horario:
                return option[1]
        return ""

    def send_email_to_client(self):
        # Obtener la fecha formateada
        fecha_cita = self.instance.fecha_cita.strftime('%d/%m/%Y')
        # Obtener el rango horario
        horario = self.get_horario_display()
        nombre_cliente = self.instance.paciente.dueño.first_name + " " + self.instance.paciente.dueño.last_name
        veterinario = self.cleaned_data["veterinario"].first_name + " " + self.cleaned_data["veterinario"].last_name  

        #código para enviar el correo electrónico
        subject = "Modificación de Agendamiento - ClinicaVet El Valle"
        message = f"""
        <html>
        <head>
        <style>
            .bold {{
                font-weight: bold;
            }}
            
            .underline {{
                text-decoration: underline;
            }}
        </style>
        </head>
        <body>
            <h2 class="bold">MODIFICACION DE AGENDAMIENTO</h2>

            <p>Estimado(a) <span class="bold">{nombre_cliente}</span>,</p>

            <p>Te informamos que tienes agendada una consulta para tu mascota "<u>{self.instance.paciente.nombre}</u>" con el veterinario {veterinario}</p>
            
            <ul>
                <li><span class="bold">Fecha y hora:</span> {fecha_cita}, a las {horario}</li>
            </ul>

            <p>Si tienes alguna pregunta o necesitas más información, no dudes en contactarnos.</p>

            <p>Atentamente,<br>
            Administración ClinicaVet El Valle</p>
        </body>
        </html>
        """
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [self.instance.paciente.dueño.email], html_message=message)

#---------------------------------------------------------------------------------#
class CitaCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['fecha_cita'].empty_label = '--- Seleccione una opción ---'
        self.fields['veterinario'].empty_label = '--- Seleccione una opción ---'
        self.fields['paciente'].empty_label = '--- Seleccione una opción ---'
        # Eliminar la primera opción del campo horario si comienza con "---------"
        first_option = self.fields['horario'].choices[0]
        if isinstance(first_option, (list, tuple)) and len(first_option) == 2 and first_option[1].startswith('---------'):
            self.fields['horario'].choices = self.fields['horario'].choices[1:]

        # Agregar la opción "Seleccione una opción" al principio
        self.fields['horario'].choices.insert(0, ('', '--- Seleccione una opción ---'))

    class Meta:
        model = Cita
        fields = ['fecha_cita', 'veterinario', 'paciente', 'horario']
        widgets = {
            'fecha_cita': DateInput(attrs={'type': 'date'})
        }
        labels = {
            'fecha_cita': 'Fecha de atención *',
            'veterinario': 'Veterinario  *',
            'paciente': 'Paciente o Mascota *',
            'horario': 'Horario de atención *',
        }


    def get_horario_display(self):
        horario = self.cleaned_data.get('horario')
        for option in Cita.HORARIOS:
            if option[0] == horario:
                return option[1]
        return ""

    def send_email_to_client(self):
        # Obtener la fecha formateada
        fecha_cita = self.instance.fecha_cita.strftime('%d/%m/%Y')
        # Obtener el rango horario
        horario = self.get_horario_display()
        nombre_cliente = self.instance.paciente.dueño.first_name + " " + self.instance.paciente.dueño.last_name
        veterinario = self.cleaned_data["veterinario"].first_name + " " + self.cleaned_data["veterinario"].last_name  

        #código para enviar el correo electrónico
        subject = "Notificación de Agendamiento - ClinicaVet El Valle"
        message = f"""
        <html>
        <head>
        <style>
            .bold {{
                font-weight: bold;
            }}
            
            .underline {{
                text-decoration: underline;
            }}
        </style>
        </head>
        <body>
            <h2 class="bold">NOTIFICACIÓN DE AGENDAMIENTO</h2>

            <p>Estimado(a) <span class="bold">{nombre_cliente}</span>,</p>

            <p>Te informamos que tienes agendada una consulta para tu mascota "<u>{self.instance.paciente.nombre}</u>" con el veterinario {veterinario}</p>
            
            <ul>
                <li><span class="bold">Fecha y hora:</span> {fecha_cita}, a las {horario}</li>
            </ul>

            <p>Si tienes alguna pregunta o necesitas más información, no dudes en contactarnos.</p>

            <p>Atentamente,<br>
            Administración ClinicaVet El Valle</p>
        </body>
        </html>
        """
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [self.instance.paciente.dueño.email], html_message=message)
#---------------------------------------------------------------------------------#

