from django.db import models
from django.core.exceptions import ValidationError
from aplicaciones.servicio.models import Servicio
from aplicaciones.cita.models import Cita
from aplicaciones.paciente.models import Paciente
from aplicaciones.accounts.models import User
from django.db import connection

# Create your models here.

def get_upload_path(instance, filename):
 # Genera un nombre de archivo único basado en el nombre del paciente
    new_filename = f'{instance.fecha_consulta}_{instance.paciente.dueño.rut}_{instance.paciente}.pdf'
    return f'documents/{new_filename}'


# Definir un validador de tamaño máximo de 1 megabytes
def validate_file_size(value):
    limit = 1024 * 1024  # Tamaño máximo de 1 MB
    if value.size > limit:
        raise ValidationError(f"El tamaño del archivo no puede exceder los {limit / (1024 * 1024)} MB.")


class ConsultaMedica(models.Model):
    fecha_consulta = models.DateField(null=True)
    horario_consulta = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='cita_consulta', null=True, verbose_name='Cita Agendada')
    peso = models.DecimalField(max_digits=6, decimal_places=1, null=True)
    altura = models.DecimalField(max_digits=5, decimal_places=1, null=True,verbose_name="Altura mascota")
    imc = models.DecimalField(verbose_name="IMC (Indice Masa Corporal)",max_digits=5, decimal_places=3, null=True)
    temperatura = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    motivo = models.CharField(max_length=500, blank=True, null=True)
    diagnostico = models.CharField(max_length=500, blank=True, null=True)
    tratamiento = models.CharField(max_length=500, blank=True, null=True)
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    veterinario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consulta_veterinario', limit_choices_to={'tipo_usuario': 'veterinario'})
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consulta_paciente')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='consulta_servicio')
    archivos_paciente = models.FileField(verbose_name='Carga Examenes', upload_to=get_upload_path, blank=True, validators=[validate_file_size])
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente
    
    # def __str__(self):
    #     return f'El paciente {self.paciente.nombre} tuvo una consulta el {self.fecha_consulta}'
    
    def __str__(self):
        if self.horario_consulta:
            return f'El paciente {self.paciente.nombre} tuvo una consulta el {self.fecha_consulta} en la cita: {self.horario_consulta}'
        else:
            return f'El paciente {self.paciente.nombre} tuvo una consulta el {self.fecha_consulta} sin cita agendada'
    
    #Definir metodo calcular IMC ejecutando el SP creado en la BD
    def calcular_imc(self):
        paciente_id = self.horario_consulta.paciente_id

        with connection.cursor() as cursor:
            cursor.callproc("SP_CALCULAR_IMC", [self.peso, self.altura, paciente_id])
            cursor.execute("COMMIT")
        
    
    def save(self, *args, **kwargs):
        if self.horario_consulta:
            self.veterinario = self.horario_consulta.veterinario
            self.paciente = self.horario_consulta.paciente
        super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     # Llamar al procedimiento para calcular el IMC
    #     calcular_imc(self.peso, self.altura, self.paciente_id)
        
    #     super().save(*args, **kwargs)



class Vacunacion(models.Model):
    consulta = models.ForeignKey('ConsultaMedica', on_delete=models.CASCADE,related_name='vacunaciones')
    nombre = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha vacunación',null=True, blank=True)

class Desparasitacion(models.Model):
    consulta = models.ForeignKey('ConsultaMedica', on_delete=models.CASCADE,related_name='desparasitaciones')
    nombre = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha desparasitación',null=True, blank=True)
    


