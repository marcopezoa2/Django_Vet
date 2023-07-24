from django.contrib import admin
from .models import Historial

# Register your models here.

class HistorialAdmin(admin.ModelAdmin):
    list_display = [
        id,'paciente' , 'fecha_creacion'
    ]

admin.site.register(Historial,HistorialAdmin)