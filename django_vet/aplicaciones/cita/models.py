import datetime
from django.db import models
# from aplicaciones.accounts.models import RelacionMascota 
from aplicaciones.paciente.models import Paciente
from django.db.models import Q
from datetime import date
from django.core.exceptions import ValidationError
from django.conf import settings
import locale
from aplicaciones.accounts.models import User


#----------------------------------------------------------------------------------------#
# Establecer la configuración regional en español de Chile
locale.setlocale(locale.LC_TIME, 'es_CL.UTF-8')

#----------------------------------------------------------------------------------------#
def validar_dia(value):
    today = date.today()
    weekday = date.fromisoformat(f'{value}').weekday()

    if value < today:
        raise ValidationError('No es posible elegir una fecha anterior a la actual')
    if (weekday == 5) or (weekday == 6):
        raise ValidationError('Elige un día laborable de la semana.')

#----------------------------------------------------------------------------------------#   

class Cita(models.Model):
    fecha_cita = models.DateField(help_text="Ingrese una fecha para el calendario", validators=[validar_dia], null=True)
    veterinario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cita_veterinario', help_text="Seleccione un veterinario", limit_choices_to={'tipo_usuario': 'veterinario'})
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='cita_paciente')
    HORARIOS = (
        ("1", "09:00"),
        ("2", "09:30"),
        ("3", "10:00"),
        ("4", "10:30"),
        ("5", "11:00"),
        ("6", "11:30"),
        ("7", "12:00"),
        ("8", "12:30"),
        ("9", "13:00"),
        ("10", "13:30"),
        ("11", "14:00"),
        ("12", "14:30"),
        ("13", "15:00"),
        ("14", "15:30"),
        ("15", "16:00"),
        ("16", "16:30"),
        ("17", "17:00"),
        ("18", "17:30"),
    )
    horario = models.CharField(max_length=10, choices=HORARIOS, null=True, help_text="Seleccione un horario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
    
    def clean(self):
        citas_mismo_horario = Cita.objects.filter(horario=self.horario, fecha_cita=self.fecha_cita, veterinario=self.veterinario)

        if citas_mismo_horario.exists():
            citas_otro_veterinario = citas_mismo_horario.exclude(veterinario=self.veterinario)

            if citas_otro_veterinario.exists():
                return

            if citas_mismo_horario.filter(veterinario=self.veterinario).exists():
                raise ValidationError('El veterinario seleccionado no está disponible en este horario')
            return
        else:
            return

    def get_paciente(self):
        return self.paciente
    
    def get_dueño(self):
        return self.paciente.dueño
    
    def __str__(self):
        fecha_formateada = self.fecha_cita.strftime('%d/%m/%Y')
        return f'{fecha_formateada} - Cliente:{self.paciente.dueño} - Paciente: {self.paciente} - Vet: {self.veterinario}'
    
    
#----------------------------------------------------------------------------------------#   

    





