from django.db import models
from django.utils import timezone

from aplicaciones.consulta.models import ConsultaMedica
from aplicaciones.accounts.models import User
from aplicaciones.paciente.models import Paciente



class Historial(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    consultas = models.ManyToManyField(ConsultaMedica,verbose_name=('Consultas Médicas'))
    # fecha_creacion = models.DateTimeField(verbose_name=('Fecha creación'),default=timezone.now)
    fecha_creacion = models.DateTimeField(verbose_name=('Fecha creación'),auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = 'Historiales'
        ordering = ['-id']  # Ordenar por el campo 'id' en orden descendente

    def __str__(self):
        if self.consultas.count() == 0:
            return f"Historial de {self.paciente.nombre} - Dueño: {self.paciente.dueño.rut}  - No hay consultas registradas"
        else:
            return f"Historial de {self.paciente.nombre} - Dueño: {self.paciente.dueño.rut}  - Consultas: {self.consultas.count()}"

    # def __str__(self):
    #     return f"Historial de {self.paciente.nombre} - Dueño: {self.dueño.user.first_name} - Consultas: {self.consultas} "