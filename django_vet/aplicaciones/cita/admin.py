from django.contrib import admin
from .models import Cita

# Register your models here.
#---------------------------------------------------------------------------------#
class CitaAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_cita', 'veterinario','paciente','horario','fecha_creacion'
    ]

#---------------------------------------------------------------------------------#
admin.site.register(Cita,CitaAdmin)
