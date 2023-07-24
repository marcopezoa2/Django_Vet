from .models import Servicio
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ServicioCreationForm,ServicioUpdateForm
from django.contrib.auth.mixins import PermissionRequiredMixin



#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Listar servicios - Uso exclusivo de administrador'''
class ServicioListView(LoginRequiredMixin,ListView,PermissionRequiredMixin):
    model = Servicio
    login_url = 'accounts:login'
    template_name = 'servicio/listar_servicio.html'
    context_object_name = 'servicio'
    paginate_by = 5
    permission_required = 'servicio.ver_servicio'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Crear servicios - Uso exclusivo de administrador'''
class ServicioCreateView(LoginRequiredMixin,CreateView,PermissionRequiredMixin):
    model = Servicio
    login_url = 'accounts:login'
    template_name = 'servicio/registro.html'
    form_class = ServicioCreationForm
    success_url = reverse_lazy('servicio:lista_servicio')
    permission_required = 'servicio.crear_servicio'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields['nombre'].widget.attrs.update({'placeholder': 'Nombre del servicio'})
    #     form.fields['descripcion'].widget.attrs.update({'placeholder': 'Descripcion'})
    #     form.fields['costo'].widget.attrs.update({'placeholder': 'Costo del servicio'})
    #     for field in form.fields:
    #         form.fields[field].widget.attrs.update({'class': 'form-control'})
    #     return form
    
    def form_valid(self, form):
        messages.success(self.request, 'El servicio se ha registrado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar el servicio.')
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase actualizar servicios - Uso exclusivo de administrador'''
class ServicioUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin):
    model = Servicio
    login_url = 'accounts:login'
    template_name = 'servicio/registro.html'
    form_class = ServicioUpdateForm
    success_url = reverse_lazy('servicio:lista_servicio')
    permission_required = 'servicio.modificar_servicio'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["nombre"].disabled = True
        return form

    def form_valid(self, form):
        messages.success(self.request, 'El servicio se ha modificado correctamente.')
        form.save()
        return redirect(self.success_url)


    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al modificar el servicio.')
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Eliminar servicios - Uso exclusivo de administrador'''
class ServicioDeleteView(DeleteView,PermissionRequiredMixin):
    model = Servicio
    login_url = 'accounts:login'
    template_name = 'servicio/servicio_confirm_delete.html'
    success_url = reverse_lazy('servicio:lista_servicio')
    permission_required = 'servicio.eliminar_servicio'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Servicio eliminado con éxito!")
        return reverse_lazy('servicio:lista_servicio')
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para buscar servicios - Uso exclusivo de administrador'''
def buscar_servicio(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese un término de búsqueda."
        return render(request, 'servicio/listar_servicio.html', {'mensaje': mensaje})
    else:
        # Dividir la consulta en palabras individuales
        palabras_clave = query.split()

        # Crear una lista de condiciones OR para cada palabra clave
        condiciones = [Q(nombre__icontains=palabra) | Q(costo__icontains=palabra) for palabra in palabras_clave]

        # Combinar las condiciones con OR utilizando el operador '|'
        query_condicion = condiciones.pop()
        for condicion in condiciones:
            query_condicion |= condicion

        # Aplicar la búsqueda utilizando las condiciones construidas
        resultados = Servicio.objects.filter(query_condicion)

        return render(request, 'servicio/listar_servicio.html', {'object_list': resultados})

#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para recargar servicios en la web - Uso exclusivo de administrador'''
def recargar_servicio(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicio/listar_servicio.html', {'object_list': servicios})

#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para publicar serrvicios en la web - Uso exclusivo de administrador'''
def publicar_servicio(request):
    if request.method == 'POST':
        form = ServicioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicio:lista_servicio')
    else:
        form = ServicioCreationForm()
    
    return render(request, 'servicio/publicar_servicio.html', {'form': form})
