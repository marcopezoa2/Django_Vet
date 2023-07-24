from django.contrib import admin
from .models import Especie,Genero,Paciente

# Register your models here.
#-------------------------------------------------------------------------------------------------------#
class EspecieAdmin(admin.ModelAdmin):
    list_display = [
        id,'nombre','fecha_creacion'
    ]
#-------------------------------------------------------------------------------------------------------#
class GeneroAdmin(admin.ModelAdmin):
    list_display = [
        id,'nombre','fecha_creacion'
    ]
#-------------------------------------------------------------------------------------------------------#
class PacienteAdmin(admin.ModelAdmin):
    list_display = [
        id,'dueño','nombre','raza','edad','fecha_nac','nro_chip','foto','color','fallecido','extraviado','activo','especie','genero','fecha_creacion'
    ]
#-------------------------------------------------------------------------------------------------------#
admin.site.register(Especie,EspecieAdmin)
admin.site.register(Genero,GeneroAdmin)
admin.site.register(Paciente,PacienteAdmin)
