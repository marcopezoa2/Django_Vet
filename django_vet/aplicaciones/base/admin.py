from django.contrib import admin
# Importe archivo 'models.py'
from .models import ContactoModel, SuscripcionModel

# Registro Modelos en el Admin
class ContactoAdmin(admin.ModelAdmin):
    search_fields = ['id','nombre', 'correo', 'asunto']
    list_display = ('id','nombre', 'correo', 'asunto', 'estado','fecha_creacion')

admin.site.register(ContactoModel, ContactoAdmin)
admin.site.register(SuscripcionModel)
