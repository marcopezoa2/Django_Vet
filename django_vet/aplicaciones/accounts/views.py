
from django.forms import ValidationError
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.views.generic.edit import CreateView
from django.views.generic import CreateView, UpdateView, FormView, DetailView, ListView, DeleteView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import (LoginView, LogoutView)
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.password_validation import get_default_password_validators
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import ClienteCreationForm, ClienteUpdateForm, EmpleadoCreationForm, EmpleadoUpdateForm, UserAdminCreationForm, UserUpdateForm
# , HorarioForm
from datetime import timedelta
from aplicaciones.accounts import forms
from .models import User
from .forms import UserImageForm
from .utils import validar_rut
import re

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views import View



'''Importaciones para generar un PDF'''
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from datetime import datetime
import io

#----------------------------------------------------------------------------------------#
'''Importaciones para generar otro PDF'''
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.decorators.http import require_POST
#----------------------------------------------------------------------------------------#
'''Importaciones para generar reporte en excel'''
import xlwt


# Create your views here.


class IndexView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/index.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_object(self):
        return self.request.user
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Permite loguearse al usuario en la aplicación - Uso todos los usuarios'''
class Login(LoginView):
    template_name = 'accounts/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Si hay un usuario logueado
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        remember_me = request.COOKIES.get('remember_me')
        if remember_me:
            kwargs['initial'] = {'username': remember_me}

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            max_age = 60 * 60 * 24 * 7  # Una semana en segundos
            expires = timezone.now() + timedelta(seconds=max_age)
            response = super().form_valid(form)
            response.set_cookie('remember_me', form.cleaned_data['username'], max_age=max_age, expires=expires, samesite='Lax')
            return response

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _('¡Inicio de sesión exitoso!'))
        return super().get_success_url()
#------------------------------------------------------------------------------------------------------------------------------#
'''Permite cerrar sesión correctamente - Uso todos los usuarios'''
class Logout(LogoutView):
    template_name = 'accounts/logged_out.html'
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para actualizar contraseña de acceso, Usuarios registrados'''
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/update_password.html'
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('accounts:index')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Contraseña cambiada correctamente. Porfavor, inicie sesión nuevamente')
        return super(UpdatePasswordView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al cambiar la contraseña.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para recuperar contraseña de acceso, envia notificacion por correo - Usuarios registrados'''
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Restablecimiento de contraseña solicitado"
                    email_template_name = "accounts/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'ClinicaVet El Valle',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "django.veterinaria.el.valle@gmail.com",
                            [user.email],
                            fail_silently=False
                        )
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    
                return redirect('accounts:password_reset_done')
            else:
                messages.error(request, "El correo electrónico ingresado no es válido o no está asociado a ninguna cuenta de ClinicaVet.")
        else:
            messages.error(request, "Ingrese un correo electrónico válido.")
    else:
        form = PasswordResetForm()

    return render(
        request=request, 
        template_name="accounts/password/password_reset.html",
        context={
            "form": form,
        })
#------------------------------------------------------------------------------------------------------------------------------#
'''Registro de usuario tipo Cliente - Uso exclusivo del Cliente por medio de HTML Registro'''

class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        rut = form.cleaned_data['rut']
        telefono = form.cleaned_data['telefono']

        # Verificar si ya existe un usuario con el mismo RUT
        existing_user = User.objects.filter(rut=rut).exists()
        if existing_user:
            messages.error(self.request, "El RUT ya está registrado. Proporcione un RUT válido.")
            return super().form_invalid(form)
        
        # Verificar si el campo está escrito
        if telefono:
            # Aplicar la validación de la expresión regular
            if not re.match(r'^\+56[1-9][0-9]{8}$', telefono):
                messages.error(self.request, "El número de teléfono no es válido. Proporcione un número de teléfono válido.")
                return self.form_invalid(form)

        # Crea el objeto User y lo guarda en la base de datos
        user = form.save(commit=False)
        user.rut = rut
        user.save()

        # Asigna el grupo de 'Cliente' al usuario
        group, created = Group.objects.get_or_create(name='Cliente')
        user.groups.add(group)
        user.save()

        messages.info(
            self.request, "¡Registro realizado con éxito! Porfavor, Inicie sesión."
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrarse. Porfavor intente nuevamente')
        return super().form_invalid(form)


#------------------------------------------------------------------------------------------------------------------------------#
'''Actualiza los datos del usuario - Uso exclusivo del Usuario(Todos)'''
# class UpdateUserView(LoginRequiredMixin, UpdateView):
#     model = User
#     login_url = reverse_lazy('accounts:login')
#     template_name = 'accounts/update_user.html'
#     fields = ['rut', 'first_name', 'last_name', 'username', 'email', 'telefono', 'direccion', 'comuna','tipo_usuario', 'is_staff', 'is_active']
#     success_url = reverse_lazy('accounts:index')

#     def get_object(self):
#         return self.request.user
    
#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         if not self.request.user.is_superuser:
#             # Campos desabilitados para su manipulación
#             form.fields['rut'].disabled = True
#             form.fields['first_name'].disabled = True
#             form.fields['last_name'].disabled = True
#             form.fields['tipo_usuario'].disabled = True
#             form.fields['is_staff'].disabled = True
#             form.fields['is_active'].disabled = True
#         return form

class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/update_user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Campos deshabilitados para su manipulación
            form.fields['rut'].disabled = True
            form.fields['first_name'].disabled = True
            form.fields['last_name'].disabled = True
            form.fields['tipo_usuario'].disabled = True
            form.fields['is_staff'].disabled = True
            form.fields['is_active'].disabled = True
        return form
    
    def form_valid(self, form):
        telefono = form.cleaned_data['telefono']

        # Verificar si el campo está escrito
        if telefono:
            # Aplicar la validación de la expresión regular
            if not re.match(r'^\+56[1-9][0-9]{8}$', telefono):
                messages.error(self.request, "El número de teléfono no es válido. Proporcione un número de teléfono válido.")
                return self.form_invalid(form)
        
        messages.success(self.request, 'Datos actualizados correctamente.')
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al actualizar los datos.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#
'''Muestra la lista de clientes registrados en sistema - Uso exclusivo del Administrador/Recepcionista'''
class ClienteListView(LoginRequiredMixin,ListView,PermissionRequiredMixin):
    model = User
    login_url = 'accounts:login'
    template_name = 'cliente/listar_cliente.html'
    context_object_name = 'cliente'
    paginate_by = 15
    permission_required = 'accounts.ver_usuario'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(tipo_usuario='cliente')
#------------------------------------------------------------------------------------------------------------------------------#
'''Registra a nuevos clientes - Uso exclusivo del Administrador/Recepcionista'''
class RegisterClienteView(CreateView):
    model = User
    template_name = 'cliente/registro.html'
    form_class = ClienteCreationForm
    success_url = reverse_lazy('accounts:lista_cliente')
    permission_required = 'accounts.crear_user'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        rut = form.cleaned_data['rut']
        telefono = form.cleaned_data['telefono']
        
        # Verificar si el campo está escrito
        if telefono:
            # Aplicar la validación de la expresión regular
            if not re.match(r'^\+56[1-9][0-9]{8}$', telefono):
                messages.error(self.request, "El número de teléfono no es válido. Proporcione un número de teléfono válido.")
                return self.form_invalid(form)

        # Verificar si ya existe un usuario con el mismo RUT
        existing_user = User.objects.filter(rut=rut).exists()
        if existing_user:
            messages.error(self.request, "El RUT ya está registrado. Proporcione un RUT válido.")
            return super().form_invalid(form)

        user = form.save(commit=False)
        user.rut = rut
        user.save()
        
        # Crea el objeto User y lo guarda en la base de datos
        user.tipo_usuario = 'cliente'  # Establece el tipo de usuario como 'cliente'

        # Asigna el grupo de 'Cliente' al usuario
        group, created = Group.objects.get_or_create(name='Cliente')
        user.groups.add(group)

        # Genera una contraseña automática
        password = User.objects.make_random_password()
        validators = get_default_password_validators()
        errors = validators[0].validate(password)
        while errors:
            password = User.objects.make_random_password()
            errors = validators[0].validate(password)

        # Establece la contraseña generada para el usuario
        user.set_password(password)
        user.save()

        #Envia un correo con una nueva contraseña al cliente
        send_mail(
            'Contraseña de registro',
            f'Se ha generado una contraseña automáticamente para su cuenta:\n\n-Contraseña: {password}\n\nPor favor, cambie su contraseña después de iniciar sesión.\n\n\n\nAtentamente,\n\nEl equipo de Clinica El Valle',
            'django.veterinaria.el.valle@gmail.com',  # Cambiar por tu dirección de correo electrónico
            [user.email],  # Dirección de correo electrónico del usuario
            fail_silently=False
        )
        messages.success(self.request, "¡Cliente registrado exitosamente! Se ha enviado la contraseña por correo electrónico.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar al cliente.')
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------#
'''Actualiza los datos de clientes registrados - Uso exclusivo del Administrador/Recepcionista'''
class ClienteUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin):
    model = User
    login_url = 'accounts:login'
    template_name = 'cliente/registro.html'
    form_class = ClienteUpdateForm
    success_url = reverse_lazy('accounts:lista_cliente')
    permission_required = 'accounts.modificar_user'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["rut"].disabled = True
            form.fields["first_name"].disabled = True
            form.fields["last_name"].disabled = True
        return form

    def form_valid(self, form):
        telefono = form.cleaned_data['telefono']
        
        # Verificar si el campo está escrito
        if telefono:
            # Aplicar la validación de la expresión regular
            if not re.match(r'^\+56[1-9][0-9]{8}$', telefono):
                messages.error(self.request, "El número de teléfono no es válido. Proporcione un número de teléfono válido.")
                return self.form_invalid(form)
        
        user = form.save(commit=False)
        user.tipo_usuario = 'cliente'  # Establece el tipo de usuario como 'cliente'
        # Asigna el grupo de 'Cliente' al usuario
        group, created = Group.objects.get_or_create(name='Cliente')
        user.groups.add(group)

        messages.success(self.request, 'El cliente se ha modificado correctamente.')
        form.save()
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al modificar al cliente.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#

from django.http import HttpResponseServerError



'''Elimina a clientes registrados - Uso exclusivo del Administrador/Recepcionista'''
class ClienteDeleteView(DeleteView,PermissionRequiredMixin):
    model = User
    login_url = 'accounts:login'
    template_name = 'cliente/cliente_confirm_delete.html'
    success_url = reverse_lazy('accounts:lista_cliente')
    permission_required = 'accounts.eliminar_user'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Cliente eliminado con éxito!")
        return reverse_lazy('accounts:lista_cliente')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, "Error al eliminar el cliente.")
            return HttpResponseServerError("Error al eliminar el cliente: {}".format(str(e)))
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para buscar clientes registrados - Uso exclusivo del Administrador/Recepcionista'''
def buscar_cliente(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese los parametros requeridos."
        return render(request, 'cliente/listar_cliente.html', {'mensaje': mensaje})
    else:
        resultados = User.objects.filter(Q(rut__icontains=query) |
                                        Q(first_name__icontains=query) |
                                        Q(last_name__icontains=query) |
                                        Q(email__icontains=query),
                                        Q(tipo_usuario='cliente'))
        return render(request, 'cliente/listar_cliente.html', {'object_list': resultados})
#------------------------------------------------------------------------------------------------------------------------------#
'''Recarga la lista de clientes registrados - Uso exclusivo del Administrador/Recepcionista'''
def recargar_cliente(request):
    clientes = User.objects.all()
    return render(request, 'cliente/listar_cliente.html', {'object_list': clientes})

#------------------------------------------------------------------------------------------------------------------------------#
'''Muestra la lista de empleados registrados - Uso exclusivo del Administrador'''

class EmpleadoListView(LoginRequiredMixin,ListView,PermissionRequiredMixin):
    model = User
    login_url = 'accounts:login'
    template_name = 'empleado/listar_empleado.html'
    context_object_name = 'veterinario'
    paginate_by = 15
    permission_denied_message = "No tienes los permisos necesarios para acceder a esta página."
    permission_required = 'accounts.ver_usuario'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(Q(tipo_usuario='veterinario') | Q(tipo_usuario='recepcionista') | Q(tipo_usuario='administrador'))
# class EmpleadoListView(LoginRequiredMixin, ListView):
#     model = get_user_model()
#     template_name = 'empleado/listar_empleado.html'
#     context_object_name = 'veterinario'
#     paginate_by = 15
#     login_url = 'accounts:login'
#     permission_denied_message = "No tienes los permisos necesarios para acceder a esta página."

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(Q(tipo_usuario='veterinario') | Q(tipo_usuario='recepcionista'))
#         return queryset
#------------------------------------------------------------------------------------------------------------------------------#
'''Registra a empleados en sistema - Uso exclusivo del Administrador'''
# class RegisterEmpleadoView(CreateView):
#     model = User
#     template_name = 'empleado/registro.html'
#     form_class = EmpleadoCreationForm
#     success_url = reverse_lazy('accounts:lista_empleado')

#     def form_valid(self, form):
#         # Crea el objeto User y lo guarda en la base de datos
#         user = form.save(commit=False)
#         tipo_usuario = form.cleaned_data['tipo_usuario']
#         if tipo_usuario in ['veterinario', 'recepcionista']:
#             user.tipo_usuario = tipo_usuario
#         user.save()

#         # Genera una contraseña automática
#         password = User.objects.make_random_password()
#         validators = get_default_password_validators()
#         errors = validators[0].validate(password)
#         while errors:
#             password = User.objects.make_random_password()
#             errors = validators[0].validate(password)

#         # Establece la contraseña generada para el usuario
#         user.set_password(password)
#         user.save()

#         #Envia un correo al usuario con su primera contraseña para iniciar sesion
#         send_mail(
#             'Contraseña de registro',
#             f'Se ha generado una contraseña automáticamente para su cuenta:\n\n-Contraseña: {password}\n\nPor favor, cambie su contraseña después de iniciar sesión.\n\n\n\nAtentamente,\n\nEl equipo de Clinica El Valle',
#             'django.veterinaria.el.valle@gmail.com',  # Cambiar por tu dirección de correo electrónico
#             [user.email],  # Dirección de correo electrónico del usuario
#             fail_silently=False
#         )
#         messages.info(
#             self.request, "Empleado registrado exitosamente! Se ha enviado la contraseña por correo electrónico."
#         )
#         return super().form_valid(form)
    
class RegisterEmpleadoView(CreateView,PermissionRequiredMixin):
    model = User
    template_name = 'empleado/registro.html'
    form_class = EmpleadoCreationForm
    success_url = reverse_lazy('accounts:lista_empleado')
    permission_required = 'accounts.crear_user'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        rut = form.cleaned_data['rut']
        telefono = form.cleaned_data['telefono']
        
        # Verificar si el campo está escrito
        if telefono:
            # Aplicar la validación de la expresión regular
            if not re.match(r'^\+56[1-9][0-9]{8}$', telefono):
                messages.error(self.request, "El número de teléfono no es válido. Proporcione un número de teléfono válido.")
                return self.form_invalid(form)

        # Verificar si ya existe un usuario con el mismo RUT
        existing_user = User.objects.filter(rut=rut).exists()
        if existing_user:
            messages.error(self.request, "El RUT ya está registrado. Proporcione un RUT válido.")
            return super().form_invalid(form)

        user = form.save(commit=False)
        user.rut = rut
        user.save()
   

        tipo_usuario = form.cleaned_data['tipo_usuario']
        if tipo_usuario == 'veterinario':
            group, created = Group.objects.get_or_create(name='Veterinario')
            user.groups.add(group)
        elif tipo_usuario == 'recepcionista':
            group, created = Group.objects.get_or_create(name='Recepcionista')
            user.groups.add(group)
        elif tipo_usuario == 'administrador':
            group, created = Group.objects.get_or_create(name='Administrador')
            user.groups.add(group)
        else:
            group, created = Group.objects.get_or_create(name='Cliente')
            user.groups.add(group)

        user.save()

        # Genera una contraseña automática
        password = User.objects.make_random_password()
        validators = get_default_password_validators()
        errors = validators[0].validate(password)
        while errors:
            password = User.objects.make_random_password()
            errors = validators[0].validate(password)

        # Establece la contraseña generada para el usuario
        user.set_password(password)
        user.save()

        #Envia un correo al usuario con su primera contraseña para iniciar sesion
        send_mail(
            'Contraseña de registro',
            f'Se ha generado una contraseña automáticamente para su cuenta:\n\n-Contraseña: {password}\n\nPor favor, cambie su contraseña después de iniciar sesión.\n\n\n\nAtentamente,\n\nEl equipo de Clinica El Valle',
            'django.veterinaria.el.valle@gmail.com',  # Cambiar por tu dirección de correo electrónico
            [user.email],  # Dirección de correo electrónico del usuario
            fail_silently=False
        )
        messages.success(
            self.request, "Empleado registrado exitosamente! Se ha enviado la contraseña por correo electrónico."
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar al empleado.')
        return super().form_invalid(form)
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Actualiza los datos de empleados registrados - Uso exclusivo del Administrador'''
class EmpleadoUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin):
    model = User
    login_url = 'accounts:login'
    template_name = 'empleado/registro.html'
    form_class = EmpleadoUpdateForm
    success_url = reverse_lazy('accounts:lista_empleado')
    permission_required = 'accounts.modificar_user'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["rut"].disabled = True
            form.fields["first_name"].disabled = True
            form.fields["last_name"].disabled = True
        return form
    
    def form_valid(self, form):
        telefono = form.cleaned_data['telefono']
        
        # Verificar si el campo está escrito
        if telefono:
            # Aplicar la validación de la expresión regular
            if not re.match(r'^\+56[1-9][0-9]{8}$', telefono):
                messages.error(self.request, "El número de teléfono no es válido. Proporcione un número de teléfono válido.")
                return self.form_invalid(form)
        
        user = form.save(commit=False)

        tipo_usuario = form.cleaned_data['tipo_usuario']
        if tipo_usuario == 'veterinario':
            group, created = Group.objects.get_or_create(name='Veterinario')
            user.groups.add(group)
        elif tipo_usuario == 'recepcionista':
            group, created = Group.objects.get_or_create(name='Recepcionista')
            user.groups.add(group)
        elif tipo_usuario == 'administrador':
            group, created = Group.objects.get_or_create(name='Administrador')
            user.groups.add(group)
        else:
            group, created = Group.objects.get_or_create(name='Cliente')
            user.groups.add(group)

        messages.success(self.request, 'El empleado se ha modificado correctamente.')
        form.save()
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al modificar al empleado.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#
'''Elimina empleados registrados - Uso exclusivo del Administrador'''
class EmpleadoDeleteView(DeleteView,PermissionRequiredMixin):
    model = User
    login_url = 'accounts:login'
    template_name = 'empleado/empleado_confirm_delete.html'
    success_url = reverse_lazy('accounts:lista_empleado')
    permission_required = 'accounts.eliminar_user'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Empleado eliminado con éxito!")
        return reverse_lazy('accounts:lista_empleado')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, "Error al eliminar el empleado.")
            return HttpResponseServerError("Error al eliminar el empleado: {}".format(str(e)))
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion de busqueda de empleados registrados - Uso exclusivo del Administrador'''
def buscar_empleado(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese los parámetros requeridos."
        return render(request, 'empleado/listar_empleado.html', {'mensaje': mensaje})
    else:
        resultados = User.objects.filter(Q(rut__icontains=query) |
                                        Q(first_name__icontains=query) |
                                        Q(last_name__icontains=query),
                                        Q(tipo_usuario='veterinario'))
        return render(request, 'empleado/listar_empleado.html', {'object_list': resultados})
#------------------------------------------------------------------------------------------------------------------------------#
'''Recarga la lista de empleados registrados - Uso exclusivo del Administrador'''
def recargar_empleado(request):
    empleados = User.objects.all()
    return render(request, 'empleado/listar_empleado.html', {'object_list': empleados})

#------------------------------------------------------------------------------------------------------------------------------#
'''Definicion de vistas URLS'''

login = Login.as_view()
register = RegisterView.as_view()
update_user = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()
index = IndexView.as_view()
#------------------------------------------------------------------------------------------------------------------------------#
'''Carga imagen de perfil - Uso exclusivo de usuarios logueados'''

class UserImageUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserImageForm
    template_name = 'accounts/user_image_update.html'
    success_url = reverse_lazy('accounts:index')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Imagen de perfil actualizada.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al actualizar la imagen de perfil.')
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------#
'''Desactivar al usuario en vez de eliminarlo - Uso exclusivo de Administrador/Recepcionista'''
def desactivar_cliente(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = False
    user.save()

    return redirect('accounts:lista_cliente')
#------------------------------------------------------------------------------------------------------------------------------#
'''Desactivar al usuario en vez de eliminarlo - Uso exclusivo de Administrador/Recepcionista'''
def activar_cliente(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = True
    user.save()

    return redirect('accounts:lista_cliente')
#------------------------------------------------------------------------------------------------------------------------------#
'''Desactivar al usuario en vez de eliminarlo - Uso exclusivo de Administrador'''
def desactivar_empleado(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = False
    user.save()

    return redirect('accounts:lista_empleado')

#------------------------------------------------------------------------------------------------------------------------------#
'''Desactivar al usuario en vez de eliminarlo - Uso exclusivo de Administrador'''
def activar_empleado(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = True
    user.save()

    return redirect('accounts:lista_empleado')

#------------------------------------------------------------------------------------------------------------------------------#


#------------------------------------------------------------------------------------------------------------------------------#

def permisos_insuficientes(request):
    return render(request, 'accounts/permisos_insuficientes.html')


#------------------------------------------------------------------------------------------------------------------------------#




def reporte_clientes(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        clientes = User.objects.filter(tipo_usuario='cliente', date_joined__range=[fecha_inicio, fecha_fin])
        total_clientes = clientes.count()

        # renderiza una plantilla HTML con los datos del informe
        return render(request, 'cliente/reporte_clientes.html', {'clientes': clientes, 'total_clientes': total_clientes})

    return redirect('accounts:listar_cliente')


#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para generar un PDF a partir del HTML que se muestra en pantalla'''
@require_POST
def generar_pdf(request):
    # Obtén los datos necesarios para el informe de cliente
    fecha_inicio = request.POST.get('fecha_inicio')
    fecha_fin = request.POST.get('fecha_fin')

    clientes = User.objects.filter(tipo_usuario='cliente', date_joined__range=[fecha_inicio, fecha_fin])
    total_clientes = clientes.count()

    # Crear el objeto PDF utilizando SimpleDocTemplate con orientación horizontal
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_clientes.pdf"'
    result_pdf = BytesIO()
    doc = SimpleDocTemplate(result_pdf, pagesize=landscape(letter))

    # Definir estilos de texto
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Title']
    estilo_titulo.alignment = 1
    estilo_titulo.fontName = 'Helvetica-Bold'
    estilo_parrafo = styles['BodyText']
    estilo_parrafo.fontName = 'Helvetica'
    estilo_parrafo.alignment = 4  # Justificación: 0=izquierda, 1=centro, 2=derecha, 4=justificado
    estilo_parrafo.spaceAfter = 12  # Espacio después del párrafo
    estilo_texto_celda = ParagraphStyle(
        'TextoCelda',
        parent=estilo_parrafo,
        alignment=4,  # Justificación: 0=izquierda, 1=centro, 2=derecha, 4=justificado
    )
    estilo_subtitulo = styles['BodyText']
    estilo_subtitulo.fontName = 'Helvetica-Bold'
    estilo_subtitulo.fontSize = 10
    estilo_subtitulo.alignment = 0  # Justificación: 0=izquierda, 1=centro, 2=derecha, 4=justificado
    
    # Calcular el ancho de la página
    page_width, page_height = landscape(letter)
    table_width = page_width - (2 * inch)  # Margen izquierdo y derecho de 1 pulgada
    # Calcular el ancho proporcional para cada columna
    column_widths = [table_width * 0.2, table_width * 0.2, table_width * 0.2, table_width * 0.3, table_width * 0.1]  

    # Definir el estilo de la tabla
    tabla_estilo = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), 'ON'),  # Permite el flujo de texto dentro de las celdas
        ('ROWHEIGHT', (0, 0), (-1, -1), 12),  # Establece el alto de las filas en 12 unidades
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),#varible de tamaño letra titular tabla
        ('BOTTOMPADDING', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crear la tabla con los datos de las clientes
    datos = [['Fecha de Creación', 'Rut', 'Nombre cliente', 'Correo', 'Comuna']]
    for cliente in clientes:
        date_joined = cliente.date_joined.strftime('%d/%m/%Y')
        nombre_completo = cliente.first_name + ' ' + cliente.last_name
        datos.append([
            date_joined,
            cliente.rut,
            nombre_completo,
            cliente.email,
            cliente.comuna

        ])

    # Aplicar el estilo de justificación de texto a todas las celdas de texto
    for i in range(1, len(datos)):
        for j in range(len(datos[i])):
            if isinstance(datos[i][j], float):
                datos[i][j] = Paragraph('{:.2f}'.format(datos[i][j]), estilo_texto_celda)  # Formatear como número con 2 decimales
            else:
                datos[i][j] = Paragraph(str(datos[i][j]), estilo_texto_celda)

    table = Table(datos, colWidths=column_widths)
    table.setStyle(tabla_estilo)  # Aplicar los estilos de la tabla definidos anteriormente

    # Construir el contenido del PDF
    content = []
    content.append(Paragraph('Reporte de Clientes', estilo_titulo))
    content.append(Paragraph(f'Total de clientes del rango seleccionado: {total_clientes}', estilo_subtitulo))
    content.append(table)

    # Agregar fecha y hora de creación al final de la página
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_joined = Paragraph(f"Fecha y hora de creación: {now}", estilo_parrafo)
    content.append(date_joined)

    # Construir el PDF y escribirlo en la respuesta
    doc.build(content)
    response.write(result_pdf.getvalue())

    return response


#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion que genera un reporte de clientes medicas en EXCEL - Uso exclusivo del Administrador/Veterinario'''
def generar_reporte_excel(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Columnas
        columns = ['Fecha de Creación', 'Tipo usuario', 'RUT', 'Nombre', 'Apellido', 'Username', 'Correo', 'Dirección', 'Comuna', 'Telefono', '¿Esta activo?']

        # Obtener los datos de Cliente en el rango especificado
        clientes = User.objects.filter(tipo_usuario='cliente', date_joined__range=[fecha_inicio, fecha_fin]).values(
            'date_joined',
            'tipo_usuario',
            'rut',
            'first_name',
            'last_name',
            'username',
            'email',
            'direccion',
            'comuna',
            'telefono',
            'is_active'
        )

        # Generar el reporte en Excel usando los valores de fecha_inicio y fecha_fin

        # Devolver el informe en Excel como respuesta
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reporte_clientes.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Cliente Data')

        # Estilo de fuente para el encabezado
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        # Escribir el título
        ws.write_merge(0, 0, 0, len(columns) - 1, 'Reporte de Clientes', font_style)

        # Escribir el total de clientes del rango seleccionado
        ws.write_merge(1, 1, 0, len(columns) - 1, f'Total de clientes del rango seleccionado: {clientes.count()}', font_style)

        # Escribir encabezados
        for col_num, column in enumerate(columns):
            ws.write(2, col_num, column, font_style)

        # Estilo de fuente para los datos
        font_style = xlwt.XFStyle()

        # Formato de fecha
        date_format = xlwt.easyxf(num_format_str='DD/MM/YYYY')

        # Escribir los datos en el archivo
        for row_num, cliente in enumerate(clientes, start=3):
            date_joined = cliente['date_joined'].strftime('%d/%m/%Y')
            ws.write(row_num, 0, date_joined, date_format)
            ws.write(row_num, 1, cliente['tipo_usuario'], font_style)
            ws.write(row_num, 2, cliente['rut'], font_style)
            ws.write(row_num, 3, cliente['first_name'], font_style)
            ws.write(row_num, 4, cliente['last_name'], font_style)
            ws.write(row_num, 5, cliente['username'], font_style)
            ws.write(row_num, 6, cliente['email'], font_style)
            ws.write(row_num, 7, cliente['direccion'], font_style)
            ws.write(row_num, 8, cliente['comuna'], font_style)
            ws.write(row_num, 9, cliente['telefono'], font_style)
            ws.write(row_num, 10, cliente['is_active'], font_style)

        # Agregar la fecha y hora de creación al final de la página
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.write(row_num + 1, 0, f"Fecha y hora de creación: {now}", font_style)

        wb.save(response)

        return response













# '''Funcion para asignar horarios a los veterinarios'''
# def asignar_horarios(request):
#     if request.method == 'POST':
#         form = HorarioForm(request.POST)
#         if form.is_valid():
#             horario = form.save()
#             messages.success(request, 'Horario creado con exito')
#             return redirect('index')
#         else:
#             messages.error(request, 'Todos los campos son requeridos')
#     else:
#         form = HorarioForm()

#     veterinarios = User.objects.all()
#     print(veterinarios)
#     return render(request, 'accounts/asignar_horarios.html', {'form': form, 'veterinarios': veterinarios})
# #------------------------------------------------------------------------------------------------------------------------------#
# '''Listar todos los horarios de los veterinarios'''
# class HorarioListView(LoginRequiredMixin,ListView):
#     model = Horario
#     login_url = 'accounts:login'
#     template_name = 'horario/listar_horario.html'
#     context_object_name = 'horario'
#     paginate_by = 10
# #------------------------------------------------------------------------------------------------------------------------------#
# '''Crear horarios para los veterinarios'''
# class HorarioCreateView(LoginRequiredMixin,CreateView):
#     model = Horario
#     login_url = 'accounts:login'
#     template_name = 'horario/registro.html'
#     fields = ['veterinario', 'dia_de_la_semana', 'hora_inicio', 'hora_fin']
#     success_url = reverse_lazy('accounts:lista_horario')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['veterinario'].widget.attrs.update({'placeholder': 'Veterinario'})
#         form.fields['dia_de_la_semana'].widget.attrs.update({'placeholder': 'Dias de la Semana'})
#         form.fields['hora_inicio'].widget.attrs.update({'placeholder': 'Hora Inicio'})
#         form.fields['hora_fin'].widget.attrs.update({'placeholder': 'Hora fin'})
#         for field in form.fields:
#             form.fields[field].widget.attrs.update({'class': 'form-control'})
#         return form
# #------------------------------------------------------------------------------------------------------------------------------#
# '''Actualizar los horarios de los veterinarios'''
# class HorarioUpdateView(LoginRequiredMixin, UpdateView):
#     model = Horario
#     login_url = 'accounts:login'
#     template_name = 'horario/registro.html'
#     form_class = HorarioForm
#     success_url = reverse_lazy('accounts:lista_horario')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         if not self.request.user.is_superuser:
#             # Disable these fields
#             form.fields["paciente"].disabled = True
#             form.fields["dueño"].disabled = True
#         return form

#     def form_valid(self, form):
#         form.save()
#         return redirect(self.success_url) 
# #------------------------------------------------------------------------------------------------------------------------------#
# '''Eliminar los horarios de los veterinarios'''
# class HorarioDeleteView(DeleteView):
#     model = Horario
#     login_url = 'accounts:login'
#     template_name = 'horario/horario_confirm_delete.html'
#     success_url = reverse_lazy('accounts:lista_horario')

#     def get_success_url(self):
#         messages.success(self.request, "Horario eliminada con éxito!")
#         return reverse_lazy('accounts:lista_horario')
# #------------------------------------------------------------------------------------------------------------------------------#
# def buscar_horario(request):
#     query = request.GET.get('q')
#     if not query:
#         mensaje = "Por favor ingrese los parametros requeridos."
#         return render(request, 'horario/listar_horario.html', {'mensaje': mensaje})
#     else:       
#         resultados = Horario.objects.filter(Q(veterinarios__user__first_name__icontains=query) |
#                                             Q(veterinarios__user__last_name__icontains=query))
#         return render(request, 'horario/listar_horario.html', {'object_list': resultados})

# #------------------------------------------------------------------------------------------------------------------------------#
# '''Funcion para recargar la lista de horarios de los veterinarios'''
# def recargar_horario(request):
#     horarios = Horario.objects.all()
#     return render(request, 'horario/listar_horario.html', {'object_list': horarios})



# #------------------------------------------------------------------------------------------------------------------------------#
#CREACION DE GRUPOS Y PERMISOS#

from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from .forms import GroupForm
#------------------------------------------------------------------------------------------------------------------------------#
class GroupListView(ListView):
    model = Group
    template_name = 'accounts/group_list.html'
    context_object_name = 'groups'

#------------------------------------------------------------------------------------------------------------------------------#
# class GroupCreateView(View):
#     def get(self, request):
#         form = GroupForm()
#         permissions = Permission.objects.all()
#         context = {'form': form, 'permissions': permissions}
#         return render(request, 'accounts/create_group.html', context)

#     def post(self, request):
#         form = GroupForm(request.POST)
#         permissions = Permission.objects.all()

#         if form.is_valid():
#             group_name = form.cleaned_data['name']
#             permission_ids = form.cleaned_data['permissions']

#             if Group.objects.filter(name=group_name).exists():
#                 error_message = 'Ya existe un grupo con el mismo nombre.'
#                 context = {'form': form, 'permissions': permissions, 'error_message': error_message}
#                 return render(request, 'accounts/create_group.html', context)

#             group = Group.objects.create(name=group_name)
#             group.permissions.set(permission_ids)
#             messages.success(request, 'Grupo creado exitosamente.')
#             return redirect('accounts:group_list')  # Redirigir a la lista de grupos después de crear exitosamente
        
#         context = {'form': form, 'permissions': permissions}
#         return render(request, 'accounts/create_group.html', context)

class GroupCreateView(View):
    def get(self, request):
        form = GroupForm()
        # permissions = Permission.objects.all()
        permissions = Permission.objects.filter(Q(codename__startswith='ver') |
                                                Q(codename__startswith='modificar') |
                                                Q(codename__startswith='eliminar') |
                                                Q(codename__startswith='crear'))
        context = {'form': form, 'permissions': permissions}
        return render(request, 'accounts/create_group.html', context)
    def get(self, request):
        form = GroupForm()
        # permissions = Permission.objects.all()
        permissions = Permission.objects.filter(Q(codename__startswith='ver') |
                                                Q(codename__startswith='modificar') |
                                                Q(codename__startswith='eliminar') |
                                                Q(codename__startswith='crear'))
        grupos = Group.objects.all()
        context = {'form': form, 'permissions': permissions, 'grupos': grupos}
        return render(request, 'accounts/create_group.html', context)
    def post(self, request):
        form = GroupForm(request.POST)
        # permissions = Permission.objects.all()
        permissions = Permission.objects.filter(Q(codename__startswith='ver') |
                                                Q(codename__startswith='modificar') |
                                                Q(codename__startswith='eliminar') |
                                                Q(codename__startswith='crear'))
        grupos = Group.objects.all()
        if form.is_valid():
            group_name = form.cleaned_data['name']
            permission_ids = form.cleaned_data['permissions']
            if Group.objects.filter(name=group_name).exists():
                error_message = 'Ya existe un grupo con el mismo nombre.'
                context = {'form': form, 'permissions': permissions, 'grupos': grupos, 'error_message': error_message}
                return render(request, 'accounts/create_group.html', context)
            group = Group.objects.create(name=group_name)
            group.permissions.set(permission_ids)
            messages.success(request, 'Grupo creado exitosamente.')
            return redirect('accounts:group_list')
        context = {'form': form, 'permissions': permissions, 'grupos': grupos}
        return render(request, 'accounts/create_group.html', context)


# class GroupCreateViews(View):
#     def get(self, request):
#         form = GroupForm()
#         custom_permissions = Permission.objects.filter(name__startswith='puede')
#         context = {'form': form, 'permissions': custom_permissions}
#         return render(request, 'accounts/create_group.html', context)

#     def post(self, request):
#         form = GroupForm(request.POST)
#         custom_permissions = Permission.objects.filter(name__startswith='puede')

#         if form.is_valid():
#             group_name = form.cleaned_data['name']
#             permission_ids = form.cleaned_data['permissions']

#             if Group.objects.filter(name=group_name).exists():
#                 error_message = 'Ya existe un grupo con el mismo nombre.'
#                 context = {'form': form, 'permissions': custom_permissions, 'error_message': error_message}
#                 return render(request, 'accounts/create_group.html', context)

#             group = Group.objects.create(name=group_name)
#             group.permissions.set(permission_ids)

#             messages.success(request, 'Grupo creado exitosamente.')
#             return redirect('accounts:group_list')

#         context = {'form': form, 'permissions': custom_permissions}
#         return render(request, 'accounts/create_group.html', context)
#------------------------------------------------------------------------------------------------------------------------------#
class GroupUpdateViewsss(View):
    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        form = GroupForm(instance=group)
        permissions = Permission.objects.all()
        context = {'form': form, 'permissions': permissions, 'group_id': group_id}
        return render(request, 'accounts/update_group.html', context)

    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        form = GroupForm(request.POST, instance=group)
        permissions = Permission.objects.all()

        if form.is_valid():
            group_name = form.cleaned_data['name']
            permission_ids = form.cleaned_data['permissions']

            if Group.objects.filter(name=group_name).exclude(id=group_id).exists():
                error_message = 'Ya existe un grupo con el mismo nombre.'
                context = {'form': form, 'permissions': permissions, 'group_id': group_id, 'error_message': error_message}
                return render(request, 'accounts/update_group.html', context)

            group = form.save(commit=False)
            group.id = group_id
            group.save()
            group.permissions.set(permission_ids)
            messages.success(request, 'Grupo actualizado exitosamente.')
            return redirect('accounts:group_list')  # Redirigir a la lista de grupos después de actualizar exitosamente
        
        context = {'form': form, 'permissions': permissions, 'group_id': group_id}
        return render(request, 'accounts/update_group.html', context)
    
class GroupUpdateView(View):
    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        form = GroupForm(instance=group)
        group_permissions = group.permissions.all()

        permissions = Permission.objects.filter(
            Q(codename__startswith='ver') |
            Q(codename__startswith='modificar') |
            Q(codename__startswith='eliminar') |
            Q(codename__startswith='crear')
        )
        context = {'form': form, 'permissions': permissions, 'group': group, 'group_permissions': group_permissions}
        return render(request, 'accounts/update_group.html', context)

    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        form = GroupForm(request.POST, instance=group)
        group_permissions = group.permissions.all()
        permissions = Permission.objects.filter(
            Q(codename__startswith='ver') |
            Q(codename__startswith='modificar') |
            Q(codename__startswith='eliminar') |
            Q(codename__startswith='crear')
        )

        if form.is_valid():
            group_name = form.cleaned_data['name']
            permission_ids = form.cleaned_data['permissions']

            if Group.objects.filter(name=group_name).exclude(id=group_id).exists():
                error_message = 'Ya existe un grupo con el mismo nombre.'
                context = {'form': form, 'permissions': permissions, 'group': group, 'group_permissions': group_permissions, 'error_message': error_message}
                return render(request, 'accounts/update_group.html', context)

            group = form.save(commit=False)
            group.id = group_id
            group.save()
            group.permissions.set(permission_ids)

            messages.success(request, 'Grupo actualizado exitosamente.')
            return redirect('accounts:group_list')

        context = {'form': form, 'permissions': permissions, 'group': group, 'group_permissions': group_permissions}
        return render(request, 'accounts/update_group.html', context)
#------------------------------------------------------------------------------------------------------------------------------#   
class GroupDeleteView(View):
    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        group.delete()
        messages.success(request, 'Grupo eliminado exitosamente.')
        return redirect('accounts:group_list')


from .permissions import create_custom_permissions

def asignar_permisos_view(request):
    # Llama a la función create_custom_permissions()
    create_custom_permissions()

    return redirect('accounts:group_list')