from django.contrib import admin
from .models import ConsultaMedica

# Register your models here.

class ConsultaAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_consulta','horario_consulta', 'peso','altura','imc','temperatura','motivo','diagnostico','tratamiento','observaciones', 'veterinario','paciente','servicio','fecha_creacion'
    ]

admin.site.register(ConsultaMedica,ConsultaAdmin)
