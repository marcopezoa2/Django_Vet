from datetime import date
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from aplicaciones.paciente.models import Paciente
from .models import Cita
from .forms import CitaCreationForm, CitaUpdateForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from aplicaciones.accounts.models import User

from django.utils import timezone

#------------------------------------------------------------------------------------------------------------------------------#
'''Muestra la lista de citas agendadas en sistema - Uso exclusivo del Administrador/Recepcionista/Cliente/Veterinario'''
class CitaListView(LoginRequiredMixin,ListView,PermissionRequiredMixin):
    model = Cita
    login_url = 'accounts:login'
    template_name = 'cita/listar_cita.html'
    context_object_name = 'cita'
    paginate_by = 10
    permission_required = 'cita.ver_cita'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        
        if user.tipo_usuario == 'cliente':
            # El usuario es un cliente, solo muestra las citas asociadas a sus propios pacientes
            queryset = super().get_queryset().filter(paciente__dueño__exact=user)
        else:
            # El usuario es un veterinario, recepcionista o administrador
            queryset = super().get_queryset()

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paciente_id = self.kwargs['paciente_id']
    #     paciente = get_object_or_404(Paciente, id=paciente_id)
    #     context['paciente'] = paciente
    #     return context
#------------------------------------------------------------------------------------------------------------------------------#
'''Registro y agendamiento de citas - Uso exclusivo del Cliente/Recepcionista/Veterinario/Administrador - Envia notificacion por correo'''
class CitaCreateView(LoginRequiredMixin, CreateView,PermissionRequiredMixin):
    model = Cita
    login_url = 'accounts:login'
    template_name = 'cita/registro.html'
    form_class = CitaCreationForm
    success_url = reverse_lazy('cita:lista_cita')
    permission_required = 'cita.crear_cita'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        if user.tipo_usuario == 'cliente':
            # Filtra los pacientes disponibles para seleccionar solo aquellos que pertenezcan al dueño actual
            form.fields['paciente'].queryset = form.fields['paciente'].queryset.filter(dueño=user)
        elif user.tipo_usuario == 'veterinario':
            form.fields['veterinario'].queryset = User.objects.filter(id=user.id)
            
        return form
    
    def form_valid(self, form):
        response = super().form_valid(form)

        # Enviar correo electrónico al cliente
        form.send_email_to_client()

        messages.success(self.request, 'La cita se ha creado exitosamente.')  # Mensaje de éxito

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Ha ocurrido un error. Por favor, revise los campos ingresados.')
        return response
#------------------------------------------------------------------------------------------------------------------------------#
'''Actualización de citas - Uso exclusivo del Cliente/Recepcionista/Veterinario/Administrador - Envia notificacion por correo'''
class CitaUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin):
    model = Cita
    login_url = 'accounts:login'
    template_name = 'cita/registro.html'
    form_class = CitaUpdateForm
    success_url = reverse_lazy('cita:lista_cita')
    permission_required = 'cita.modificar_cita'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["paciente"].disabled = True
            # form.fields["dueño"].disabled = True
        return form
    
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     form.save()

    #     # Enviar correo electrónico al cliente
    #     form.send_email_to_client()
        
    #     messages.success(self.request, 'La cita se ha modificado exitosamente.')  # Mensaje de éxito

    #     return response

    def form_valid(self, form):
        cita = form.save(commit=False)

        if cita.fecha_cita < date.today():
            messages.error(self.request, 'No se puede modificar una cita pasada.')
            return self.form_invalid(form)

        response = super().form_valid(form)
        form.save()
        form.send_email_to_client()
        messages.success(self.request, 'La cita se ha modificado exitosamente.')

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Ha ocurrido un error. Por favor, revise los campos ingresados.')
        return response  
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Eliminación de citas - Uso exclusivo del Cliente/Recepcionista/Veterinario/Administrador'''
class CitaDeleteView(DeleteView,PermissionRequiredMixin):
    model = Cita
    login_url = 'accounts:login'
    template_name = 'cita/cita_confirm_delete.html'
    success_url = reverse_lazy('cita:lista_cita')
    permission_required = 'cita.eliminar_cita'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Cita eliminada con éxito!")
        return reverse_lazy('cita:lista_cita')
    
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para buscar citas agendadas - Uso exclusivo del Administrador/Recepcionista/Cliente/Veterinario'''   
def buscar_cita(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese un término de búsqueda."
        return render(request, 'cita/listar_cita.html', {'mensaje': mensaje})
    else:
        # Dividir la consulta en palabras individuales
        palabras_clave = query.split()

        # Crear una lista de condiciones OR para cada palabra clave
        condiciones = [(Q(fecha_cita__icontains=palabra) |
                        Q(veterinario__first_name__icontains=palabra) |
                        Q(veterinario__last_name__icontains=palabra) |
                        Q(veterinario__rut__icontains=palabra) |
                        Q(paciente__dueño__first_name__icontains=palabra) |
                        Q(paciente__dueño__last_name__icontains=palabra) |
                        Q(paciente__dueño__rut__icontains=palabra) |
                        Q(paciente__nombre__icontains=palabra)) for palabra in palabras_clave]

        # Combinar las condiciones con OR utilizando el operador '|'
        query_condicion = condiciones.pop()
        for condicion in condiciones:
            query_condicion |= condicion

        # Aplicar la búsqueda utilizando las condiciones construidas
        resultados = Cita.objects.filter(query_condicion)

        return render(request, 'cita/listar_cita.html', {'object_list': resultados})
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Recarga la lista de citas agendadas - Uso exclusivo del Administrador/Recepcionista/Veterinario'''
def recargar_cita(request):
    
    citas = Cita.objects.all()
    return render(request, 'cita/listar_cita.html', {'object_list': citas})

#------------------------------------------------------------------------------------------------------------------------------#
