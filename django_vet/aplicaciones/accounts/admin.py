from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminForm
from .models import Region, Comuna, User
#  Especialidad, Cargo,
# ,Horario

# Register your models here.

#------------------------------------------------------------------------------------------------------------------------------#

class UserAdmin(BaseUserAdmin):
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupos'

    def get_permissions(self, obj):
        return ", ".join([perm.codename for perm in obj.user_permissions.all()])
    get_permissions.short_description = 'Permisos'
    
    add_form = UserAdminCreationForm
    add_fieldsets = (
        ('Registro de Usuario', {
            'fields': ('rut','username','first_name','last_name','email','direccion','comuna','telefono','tipo_usuario','is_staff','is_active','password1', 'password2','image')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        ('Información de Acceso: ', {
            'fields': ('rut','username','tipo_usuario')
        }),
        ('Información Personal: ', {
            'fields': ('password','first_name', 'last_name', 'email','last_login','direccion','telefono','image')
        }),
        ('Permisos: ', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser','user_permissions','groups'
            )
        }),
    )

    #muestra en el display de admin django
    list_display = ['rut','tipo_usuario','first_name','last_name', 'email', 'is_active', 'is_staff','date_joined','get_groups', 'get_permissions']
#------------------------------------------------------------------------------------------------------------------------------#

'''Muestra las vistas de Django en el Administrador'''
admin.site.register(User, UserAdmin)
admin.site.register(Region)
admin.site.register(Comuna)
# admin.site.register(Especialidad)
# admin.site.register(Cargo)

'''MuestraCambios en Administrador Django'''
admin.site.site_header = 'Veterinaria El Valle'
admin.site.index_title = 'Panel de control El Valle'
admin.site.site_title = 'Titulo en la pestaña del navegador'



