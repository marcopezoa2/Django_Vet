from django.contrib import admin
from .models import Servicio
# ,TipoVacuna,Vacuna,Vacunacion,TipoDesparasitante,Desparasitante,Desparasitacion

# Register your models here.


class ServicioAdmin(admin.ModelAdmin):
    list_display = [
        id,'nombre', 'descripcion','costo','fecha_creacion'
    ]



admin.site.register(Servicio,ServicioAdmin)
# admin.site.register(TipoVacuna)
# admin.site.register(Vacuna)
# admin.site.register(Vacunacion)
# admin.site.register(TipoDesparasitante)
# admin.site.register(Desparasitante)
# admin.site.register(Desparasitacion)
