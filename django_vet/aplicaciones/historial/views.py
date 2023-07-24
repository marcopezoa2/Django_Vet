from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import ConsultaMedica, Paciente
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin



#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion de listar historial atenciones paciente - Uso exclusivo del Administrador/Veterinario/Cliente/Recepcionista'''
class HistoriaListView(ListView,PermissionRequiredMixin):
    template_name = 'historial/historial.html'
    context_object_name = 'consultas'
    permission_required = 'paciente.ver_paciente'
    raise_exception = False  # Desactiva la excepción de PermissionDenied

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a este paciente.")
        return redirect('paciente:lista_paciente')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return self.handle_no_permission()

    def get_queryset(self):
        paciente_id = self.kwargs['paciente_id']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        user = self.request.user

        if user.tipo_usuario == 'cliente':
            # El usuario es un cliente, verificar si el paciente pertenece al dueño del usuario
            if paciente.dueño != user:
                # El paciente no pertenece al usuario dueño, lanzar una excepción Http404
                raise Http404("No tienes permiso para acceder a este paciente.")

            # El paciente pertenece al usuario dueño, mostrar las consultas médicas asociadas a ese paciente
            queryset = ConsultaMedica.objects.filter(paciente=paciente)
        else:
            # El usuario es un veterinario, recepcionista o administrador
            queryset = ConsultaMedica.objects.filter(paciente=paciente)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs['paciente_id']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        context['paciente'] = paciente
        return context
'''
    def get_queryset(self):
        paciente_id = self.kwargs['paciente_id']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        user = self.request.user

        if user.tipo_usuario == 'cliente':
            # El usuario es un cliente, verificar si el paciente pertenece al dueño del usuario
            if paciente.dueño != user:
                # El paciente no pertenece al usuario dueño, lanzar una excepción Http404
                # raise Http404("No tienes permiso para acceder a este paciente.")
                messages.error(self.request, "No tienes permiso para acceder a este paciente.")
                return redirect('paciente:lista_paciente')

            # El paciente pertenece al usuario dueño, mostrar las consultas médicas asociadas a ese paciente
            queryset = ConsultaMedica.objects.filter(paciente=paciente)
        else:
            # El usuario es un veterinario, recepcionista o administrador
            queryset = ConsultaMedica.objects.filter(paciente=paciente)

        return queryset
'''  
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paciente_id = self.kwargs['paciente_id']
    #     paciente = get_object_or_404(Paciente, id=paciente_id)
    #     context['paciente'] = paciente
    #     return context
#------------------------------------------------------------------------------------------------------------------------------#




