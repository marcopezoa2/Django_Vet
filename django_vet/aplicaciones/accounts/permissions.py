# from .permissions import create_custom_permissions

# # Resto del código de configuración

# # Llamar a la función para crear los permisos personalizados
# create_custom_permissions()



from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from aplicaciones.accounts.models import User, Comuna, Region
# ,Especialidad,Cargo, 
from aplicaciones.cita.models import Cita
from aplicaciones.consulta.models import ConsultaMedica, Vacunacion, Desparasitacion
from aplicaciones.historial.models import Historial
from aplicaciones.inventario.models import Producto, RegistroUsoProducto, Categoria
from aplicaciones.paciente.models import Paciente, Especie, Genero
from aplicaciones.proveedor.models import Proveedor
from aplicaciones.servicio.models import Servicio



def create_custom_permissions():

    # # Eliminar los permisos existentes
    # Permission.objects.filter(codename__startswith='ver_paciente').delete()
    # Permission.objects.filter(codename__startswith='crear_paciente').delete()
    # Permission.objects.filter(codename__startswith='modificar_paciente').delete()
    # Permission.objects.filter(codename__startswith='eliminar_paciente').delete()


    # Obtener o crear los grupos necesarios
    grupo_cliente, created = Group.objects.get_or_create(name='Cliente')
    grupo_veterinario, created = Group.objects.get_or_create(name='Veterinario')
    grupo_recepcionista, created = Group.objects.get_or_create(name='Recepcionista')
    grupo_administrador, created = Group.objects.get_or_create(name='Administrador')

    # Obtener el contenido de los modelos necesarios para asignar permisos
    content_type_user = ContentType.objects.get_for_model(User)
    # content_type_cargo = ContentType.objects.get_for_model(Cargo)
    content_type_comuna = ContentType.objects.get_for_model(Comuna)
    content_type_region = ContentType.objects.get_for_model(Region)
    # content_type_especialidad = ContentType.objects.get_for_model(Especialidad)
    content_type_cita = ContentType.objects.get_for_model(Cita)
    content_type_consulta = ContentType.objects.get_for_model(ConsultaMedica)
    content_type_vacunacion = ContentType.objects.get_for_model(Vacunacion)
    content_type_desparasitacion = ContentType.objects.get_for_model(Desparasitacion)
    content_type_historial = ContentType.objects.get_for_model(Historial)
    content_type_producto = ContentType.objects.get_for_model(Producto)
    content_type_categoria = ContentType.objects.get_for_model(Categoria)
    content_type_consumoProducto = ContentType.objects.get_for_model(RegistroUsoProducto)
    content_type_paciente = ContentType.objects.get_for_model(Paciente)
    content_type_genero = ContentType.objects.get_for_model(Genero)
    content_type_especie = ContentType.objects.get_for_model(Especie)
    content_type_proveedor = ContentType.objects.get_for_model(Proveedor)
    content_type_servicio = ContentType.objects.get_for_model(Servicio)

###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_paciente , created = Permission.objects.get_or_create(
        codename='ver_paciente',
        name='Puede ver pacientes',
        content_type=content_type_paciente,
    )
    permission_add_paciente , created = Permission.objects.get_or_create(
        codename='crear_paciente',
        name='Puede crear pacientes',
        content_type=content_type_paciente,
    )
    permission_change_paciente , created = Permission.objects.get_or_create(
        codename='modificar_paciente',
        name='Puede modificar pacientes',
        content_type=content_type_paciente,
    )
    permission_delete_paciente , created = Permission.objects.get_or_create(
        codename='eliminar_paciente',
        name='Puede eliminar pacientes',
        content_type=content_type_paciente,
    )
###------------------------------------------------------------------------------------------------------###
    permission_view_cita , created = Permission.objects.get_or_create(
        codename='ver_cita',
        name='Puede ver citas',
        content_type=content_type_cita,
    )
    permission_add_cita , created = Permission.objects.get_or_create(
        codename='crear_cita',
        name='Puede crear citas',
        content_type=content_type_cita,
    )
    permission_change_cita , created = Permission.objects.get_or_create(
        codename='modificar_cita',
        name='Puede modificar citas',
        content_type=content_type_cita,
    )
    permission_delete_cita , created = Permission.objects.get_or_create(
        codename='eliminar_cita',
        name='Puede eliminar citas',
        content_type=content_type_cita,
    )
###------------------------------------------------------------------------------------------------------###
    permission_view_consulta , created = Permission.objects.get_or_create(
        codename='ver_consulta',
        name='Puede ver consultas',
        content_type=content_type_consulta,
    )
    permission_add_consulta , created = Permission.objects.get_or_create(
        codename='crear_consulta',
        name='Puede crear consultas',
        content_type=content_type_consulta,
    )
    permission_change_consulta , created = Permission.objects.get_or_create(
        codename='modificar_consulta',
        name='Puede modificar consultas',
        content_type=content_type_consulta,
    )
    permission_delete_consulta , created = Permission.objects.get_or_create(
        codename='eliminar_consulta',
        name='Puede eliminar consultas',
        content_type=content_type_consulta,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos para el grupo "Cliente"
    permission_view_user , created = Permission.objects.get_or_create(
        codename='ver_usuario',
        name='Puede ver usuarios',
        content_type=content_type_user,
    )
    permission_add_user , created = Permission.objects.get_or_create(
        codename='crear_user',
        name='Puede crear usuarios',
        content_type=content_type_user,
    )
    permission_change_user , created = Permission.objects.get_or_create(
        codename='modificar_user',
        name='Puede modificar usuarios',
        content_type=content_type_user,
    )
    permission_delete_user , created = Permission.objects.get_or_create(
        codename='eliminar_user',
        name='Puede eliminar usuarios',
        content_type=content_type_user,
    )
# ###------------------------------------------------------------------------------------------------------###
#     # Crear los permisos para el grupo "Cliente"
#     permission_view_cargo , created = Permission.objects.get_or_create(
#         codename='ver_cargo',
#         name='Puede ver cargos',
#         content_type=content_type_cargo,
#     )
#     permission_add_cargo , created = Permission.objects.get_or_create(
#         codename='crear_cargo',
#         name='Puede crear cargos',
#         content_type=content_type_cargo,
#     )
#     permission_change_cargo , created = Permission.objects.get_or_create(
#         codename='modificar_cargo',
#         name='Puede modificar cargos',
#         content_type=content_type_cargo,
#     )
#     permission_delete_cargo , created = Permission.objects.get_or_create(
#         codename='eliminar_cargo',
#         name='Puede eliminar cargos',
#         content_type=content_type_cargo,
#     )
# ###------------------------------------------------------------------------------------------------------###
#     # Crear los permisos para el grupo "Cliente"
#     permission_view_especialidad , created = Permission.objects.get_or_create(
#         codename='ver_especialidad',
#         name='Puede ver especialidades',
#         content_type=content_type_especialidad,
#     )
#     permission_add_especialidad , created = Permission.objects.get_or_create(
#         codename='crear_especialidad',
#         name='Puede crear especialidades',
#         content_type=content_type_especialidad,
#     )
#     permission_change_especialidad , created = Permission.objects.get_or_create(
#         codename='modificar_especialidad',
#         name='Puede modificar especialidades',
#         content_type=content_type_especialidad,
#     )
#     permission_delete_especialidad , created = Permission.objects.get_or_create(
#         codename='eliminar_especialidad',
#         name='Puede eliminar especialidades',
#         content_type=content_type_especialidad,
#     )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos para el grupo "Cliente"
    permission_view_region , created = Permission.objects.get_or_create(
        codename='ver_region',
        name='Puede ver regiones',
        content_type=content_type_region,
    )
    permission_add_region , created = Permission.objects.get_or_create(
        codename='crear_region',
        name='Puede crear regiones',
        content_type=content_type_region,
    )
    permission_change_region , created = Permission.objects.get_or_create(
        codename='modificar_region',
        name='Puede modificar regiones',
        content_type=content_type_region,
    )
    permission_delete_region , created = Permission.objects.get_or_create(
        codename='eliminar_region',
        name='Puede eliminar regiones',
        content_type=content_type_region,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_comuna , created = Permission.objects.get_or_create(
        codename='ver_comuna',
        name='Puede ver comunas',
        content_type=content_type_comuna,
    )
    permission_add_comuna , created = Permission.objects.get_or_create(
        codename='crear_comuna',
        name='Puede crear comunas',
        content_type=content_type_comuna,
    )
    permission_change_comuna , created = Permission.objects.get_or_create(
        codename='modificar_comuna',
        name='Puede modificar comunas',
        content_type=content_type_comuna,
    )
    permission_delete_comuna , created = Permission.objects.get_or_create(
        codename='eliminar_comuna',
        name='Puede eliminar comunas',
        content_type=content_type_comuna,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_vacunacion , created = Permission.objects.get_or_create(
        codename='ver_vacunacion',
        name='Puede ver vacunacion',
        content_type=content_type_vacunacion,
    )
    permission_add_vacunacion , created = Permission.objects.get_or_create(
        codename='crear_vacunacion',
        name='Puede crear vacunacion',
        content_type=content_type_vacunacion,
    )
    permission_change_vacunacion , created = Permission.objects.get_or_create(
        codename='modificar_vacunacion',
        name='Puede modificar vacunacion',
        content_type=content_type_vacunacion,
    )
    permission_delete_vacunacion , created = Permission.objects.get_or_create(
        codename='eliminar_vacunacion',
        name='Puede eliminar vacunacion',
        content_type=content_type_vacunacion,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_desparasitacion , created = Permission.objects.get_or_create(
        codename='ver_desparasitacion',
        name='Puede ver desparasitacions',
        content_type=content_type_desparasitacion,
    )
    permission_add_desparasitacion , created = Permission.objects.get_or_create(
        codename='crear_desparasitacion',
        name='Puede crear desparasitacion',
        content_type=content_type_desparasitacion,
    )
    permission_change_desparasitacion , created = Permission.objects.get_or_create(
        codename='modificar_desparasitacion',
        name='Puede modificar desparasitacion',
        content_type=content_type_desparasitacion,
    )
    permission_delete_desparasitacion , created = Permission.objects.get_or_create(
        codename='eliminar_desparasitacion',
        name='Puede eliminar desparasitacion',
        content_type=content_type_desparasitacion,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_categoria , created = Permission.objects.get_or_create(
        codename='ver_categoria',
        name='Puede ver categorias',
        content_type=content_type_categoria,
    )
    permission_add_categoria , created = Permission.objects.get_or_create(
        codename='crear_categoria',
        name='Puede crear categorias',
        content_type=content_type_categoria,
    )
    permission_change_categoria , created = Permission.objects.get_or_create(
        codename='modificar_categoria',
        name='Puede modificar categorias',
        content_type=content_type_categoria,
    )
    permission_delete_categoria , created = Permission.objects.get_or_create(
        codename='eliminar_categoria',
        name='Puede eliminar categoris',
        content_type=content_type_categoria,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_producto , created = Permission.objects.get_or_create(
        codename='ver_producto',
        name='Puede ver productos',
        content_type=content_type_producto,
    )
    permission_add_producto , created = Permission.objects.get_or_create(
        codename='crear_producto',
        name='Puede crear productos',
        content_type=content_type_producto,
    )
    permission_change_producto , created = Permission.objects.get_or_create(
        codename='modificar_producto',
        name='Puede modificar productos',
        content_type=content_type_producto,
    )
    permission_delete_producto , created = Permission.objects.get_or_create(
        codename='eliminar_producto',
        name='Puede eliminar productos',
        content_type=content_type_producto,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_consumoProducto , created = Permission.objects.get_or_create(
        codename='ver_consumoProducto',
        name='Puede ver consumo productos',
        content_type=content_type_consumoProducto,
    )
    permission_add_consumoProducto , created = Permission.objects.get_or_create(
        codename='crear_consumoProducto',
        name='Puede crear consumo productos',
        content_type=content_type_consumoProducto,
    )
    permission_change_consumoProducto , created = Permission.objects.get_or_create(
        codename='modificar_consumoProducto',
        name='Puede modificar consumo productos',
        content_type=content_type_consumoProducto,
    )
    permission_delete_consumoProducto , created = Permission.objects.get_or_create(
        codename='eliminar_consumoProductos',
        name='Puede eliminar consumo productos',
        content_type=content_type_consumoProducto,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_genero , created = Permission.objects.get_or_create(
        codename='ver_genero',
        name='Puede ver generos',
        content_type=content_type_genero,
    )
    permission_add_genero , created = Permission.objects.get_or_create(
        codename='crear_genero',
        name='Puede crear generos',
        content_type=content_type_genero,
    )
    permission_change_genero , created = Permission.objects.get_or_create(
        codename='modificar_genero',
        name='Puede modificar generos',
        content_type=content_type_genero,
    )
    permission_delete_genero , created = Permission.objects.get_or_create(
        codename='eliminar_genero',
        name='Puede eliminar generos',
        content_type=content_type_genero,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_especie , created = Permission.objects.get_or_create(
        codename='ver_especie',
        name='Puede ver especies',
        content_type=content_type_especie,
    )
    permission_add_especie , created = Permission.objects.get_or_create(
        codename='crear_especie',
        name='Puede crear especies',
        content_type=content_type_especie,
    )
    permission_change_especie , created = Permission.objects.get_or_create(
        codename='modificar_especie',
        name='Puede modificar especies',
        content_type=content_type_especie,
    )
    permission_delete_especie , created = Permission.objects.get_or_create(
        codename='eliminar_especie',
        name='Puede eliminar especies',
        content_type=content_type_especie,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_proveedor , created = Permission.objects.get_or_create(
        codename='ver_proveedor',
        name='Puede ver proveedores',
        content_type=content_type_proveedor,
    )
    permission_add_proveedor , created = Permission.objects.get_or_create(
        codename='crear_proveedor',
        name='Puede crear proveedores',
        content_type=content_type_proveedor,
    )
    permission_change_proveedor , created = Permission.objects.get_or_create(
        codename='modificar_proveedor',
        name='Puede modificar proveedores',
        content_type=content_type_proveedor,
    )
    permission_delete_proveedor , created = Permission.objects.get_or_create(
        codename='eliminar_proveedor',
        name='Puede eliminar proveedores',
        content_type=content_type_proveedor,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_servicio , created = Permission.objects.get_or_create(
        codename='ver_servicio',
        name='Puede ver servicios',
        content_type=content_type_servicio,
    )
    permission_add_servicio , created = Permission.objects.get_or_create(
        codename='crear_servicio',
        name='Puede crear servicios',
        content_type=content_type_servicio,
    )
    permission_change_servicio , created = Permission.objects.get_or_create(
        codename='modificar_servicio',
        name='Puede modificar servicios',
        content_type=content_type_servicio,
    )
    permission_delete_servicio , created = Permission.objects.get_or_create(
        codename='eliminar_servicio',
        name='Puede eliminar servicios',
        content_type=content_type_servicio,
    )
###------------------------------------------------------------------------------------------------------###
    # Crear los permisos
    permission_view_historial , created = Permission.objects.get_or_create(
        codename='ver_historial',
        name='Puede ver historials',
        content_type=content_type_historial,
    )
    permission_add_historial , created = Permission.objects.get_or_create(
        codename='crear_historial',
        name='Puede crear historial',
        content_type=content_type_historial,
    )
    permission_change_historial , created = Permission.objects.get_or_create(
        codename='modificar_historial',
        name='Puede modificar historial',
        content_type=content_type_historial,
    )
    permission_delete_historial , created = Permission.objects.get_or_create(
        codename='eliminar_historial',
        name='Puede eliminar historial',
        content_type=content_type_historial,
    )


    # Asignar los permisos al grupo "Administrador" 
    grupo_administrador.permissions.add(
#Permisos para ver
        permission_view_paciente,
        permission_view_cita,
        permission_view_user,
        # permission_view_cargo,
        # permission_view_especialidad,
        permission_view_region,
        permission_view_comuna,
        permission_view_consulta,
        permission_view_vacunacion,
        permission_view_desparasitacion,
        permission_view_categoria,
        permission_view_producto,
        permission_view_consumoProducto,
        permission_view_genero,
        permission_view_especie,
        permission_view_proveedor,
        permission_view_servicio,
        permission_view_historial,
#Permisos para crear
        permission_add_paciente,
        permission_add_cita,
        permission_add_user,
        # permission_add_cargo,
        # permission_add_especialidad,
        permission_add_region,
        permission_add_comuna,
        permission_add_consulta,
        permission_add_vacunacion,
        permission_add_desparasitacion,
        permission_add_categoria,
        permission_add_producto,
        permission_add_consumoProducto,
        permission_add_genero,
        permission_add_especie,
        permission_add_proveedor,
        permission_add_servicio,
        permission_add_historial,
#Permisos para actualizar
        permission_change_paciente,
        permission_change_cita,
        permission_change_user,
        # permission_change_cargo,
        # permission_change_especialidad,
        permission_change_region,
        permission_change_comuna,
        permission_change_consulta,
        permission_change_vacunacion,
        permission_change_desparasitacion,
        permission_change_categoria,
        permission_change_producto,
        permission_change_consumoProducto,
        permission_change_genero,
        permission_change_especie,
        permission_change_proveedor,
        permission_change_servicio,
        permission_change_historial,
#Permisos para eliminar
        permission_delete_paciente,
        permission_delete_cita,
        permission_delete_user,
        # permission_delete_cargo,
        # permission_delete_especialidad,
        permission_delete_region,
        permission_delete_comuna,
        permission_delete_consulta,
        permission_delete_vacunacion,
        permission_delete_desparasitacion,
        permission_delete_categoria,
        permission_delete_producto,
        permission_delete_consumoProducto,
        permission_delete_genero,
        permission_delete_especie,
        permission_delete_proveedor,
        permission_delete_servicio,
        permission_delete_historial
    )

    # Asignar los permisos al grupo "Veterinario"
    grupo_veterinario.permissions.add(
#Permisos para ver
        permission_view_paciente,
        permission_view_cita,
        permission_view_user,
        permission_view_consulta,
        permission_view_vacunacion,
        permission_view_desparasitacion,
        permission_view_producto,
        permission_view_consumoProducto,
        permission_view_historial,
        permission_view_servicio,
#Permisos para crear
        permission_add_paciente,
        permission_add_cita,
        permission_add_consulta,
        permission_add_vacunacion,
        permission_add_desparasitacion,
        permission_add_consumoProducto,
#Permisos para actualizar
        permission_change_paciente,
        permission_change_cita,
        permission_change_user,
        permission_change_consulta,
        permission_change_vacunacion,
        permission_change_desparasitacion,
        permission_change_consumoProducto,
#Permisos para eliminar
        permission_delete_paciente,
        permission_delete_cita,
        permission_delete_consulta,
        permission_delete_vacunacion,
        permission_delete_desparasitacion,
    )

    # Asignar los permisos al grupo "Recepcionista"
    grupo_recepcionista.permissions.add(
#Permisos para ver
        permission_view_paciente,
        permission_view_cita,
        permission_view_user,
        permission_view_consulta,
        permission_view_vacunacion,
        permission_view_desparasitacion,
        permission_view_producto,
        permission_view_consumoProducto,
        permission_view_proveedor,
        permission_view_servicio,
        permission_view_historial,
#Permisos para crear
        permission_add_paciente,
        permission_add_cita,
        permission_add_user,
#Permisos para actualizar
        permission_change_paciente,
        permission_change_cita,
        permission_change_user,
#Permisos para eliminar
        permission_delete_paciente,
        permission_delete_cita,
        permission_delete_user,
    )

    # Asignar los permisos al grupo "Cliente"
    grupo_cliente.permissions.add(
#Permisos para ver
        permission_view_paciente,
        permission_view_cita,
        permission_view_user,
        # permission_view_cargo,
        permission_view_consulta,
        permission_view_vacunacion,
        permission_view_desparasitacion,
        permission_view_historial,
#Permisos para crear
        permission_add_paciente,
        permission_add_cita,
        permission_add_user,
#Permisos para actualizar
        permission_change_paciente,
        permission_change_cita,
        permission_change_user,
#Permisos para eliminar
        permission_delete_cita,
    )



# Llamar a la función para crear los permisos personalizados
# create_custom_permissions()