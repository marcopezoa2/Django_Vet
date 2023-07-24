from django.conf import settings
from django.urls import path, reverse_lazy
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .import views
# from .views import HorarioListView, HorarioCreateView, HorarioUpdateView, HorarioDeleteView
from .views import ClienteListView, GroupCreateView, GroupDeleteView, GroupListView, GroupUpdateView,RegisterClienteView,ClienteDeleteView,  ClienteUpdateView, UserImageUpdateView, asignar_permisos_view, generar_pdf, generar_reporte_excel, reporte_clientes
from .views import EmpleadoListView,RegisterEmpleadoView,EmpleadoDeleteView,  EmpleadoUpdateView
from .views import permisos_insuficientes


app_name = 'accounts'



urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('cambiar-datos/', views.update_user, name='update_user'),
    path('cambiar-password/', views.update_password, name='update_password'),
    path('recuperar-password/',views.password_reset_request,name='password_reset'),
    path('recuperar-password-ok/', auth_views.PasswordResetDoneView.as_view (template_name='accounts/password/password_reset_done.html'), name='password_reset_done',),
    path('recuperar-password-completo/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password/password_reset_complete.html'), name='password_reset_complete',),
    path('recuperar-password-confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password/password_reset_confirm.html',success_url=reverse_lazy("accounts:password_reset_complete")),name='password_reset_confirm'),
    path('password_reset_confirm', views.password_reset_request,name="password_reset"),
    path('user/image/update/', UserImageUpdateView.as_view(), name='user_image_update'),

    path('cliente/desactivar/<int:pk>/', views.desactivar_cliente, name='desactivar_cliente'),
    path('cliente/activar/<int:pk>/', views.activar_cliente, name='activar_cliente'),

    path('empleado/desactivar/<int:pk>/', views.desactivar_empleado, name='desactivar_empleado'),
    path('empleado/activar/<int:pk>/', views.activar_empleado, name='activar_empleado'),

    path('permisos-insuficientes/', permisos_insuficientes, name='permisos_insuficientes'),
    path('asignar_permisos/', views.asignar_permisos_view, name='asignar_permisos'),
    

    # '''Path para Horarios Veterinarios'''
    # path('listar/', HorarioListView.as_view(), name='lista_horario'),
    # path('crear/', HorarioCreateView.as_view(), name='crear_horario'),
    # path('editar/<int:pk>/', HorarioUpdateView.as_view(), name='actualizar_horario'),
    # path('eliminar/<int:pk>/', HorarioDeleteView.as_view(), name='eliminar_horario'),
    # path('buscar/', views.buscar_horario, name='buscar_horario'),
    # path('listar/', views.recargar_horario, name='listar_horario'),
    # path('asignar-horarios/', views.asignar_horarios, name='asignar_horarios'),

    # '''Path CRUD Clientes'''
    path('registro-cliente/', RegisterClienteView.as_view(), name='crear_cliente'),
    path('listar-cliente/', ClienteListView.as_view(), name='lista_cliente'),
    path('editar-cliente/<int:pk>/', ClienteUpdateView.as_view(), name='actualizar_cliente'),
    path('eliminar-cliente/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('listar-cliente/', views.recargar_cliente, name='listar_cliente'),

    # '''Path CRUD Empleados'''
    path('registro-empleado/', RegisterEmpleadoView.as_view(), name='crear_empleado'),
    path('listar-empleado/', EmpleadoListView.as_view(), name='lista_empleado'),
    path('editar-empleado/<int:pk>/', EmpleadoUpdateView.as_view(), name='actualizar_empleado'),
    path('eliminar-empleado/<int:pk>/', EmpleadoDeleteView.as_view(), name='eliminar_empleado'),
    path('buscar-empleado/', views.buscar_empleado, name='buscar_empleado'),
    path('listar-empleado/', views.recargar_empleado, name='listar_empleado'),


    path('reporte/', reporte_clientes, name='reporte_clientes'),
    path('generar_pdf', generar_pdf, name='generar_pdf'),
    path('reporte/excel/', generar_reporte_excel, name='generar_reporte_excel'),

    path('grupo/crear/', GroupCreateView.as_view(), name='crear_grupo'),
    path('grupo/lista/', GroupListView.as_view(), name='group_list'),
    path('grupo/<int:group_id>/actualizar/', GroupUpdateView.as_view(), name='group_update'),
    path('grupo/<int:group_id>/eliminar/', GroupDeleteView.as_view(), name='group_delete'),


]

#Se utiliza para habilitar el modo de depuración durante el desarrollo de la aplicación
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
