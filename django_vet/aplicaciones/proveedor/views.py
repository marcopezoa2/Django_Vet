from .models import Proveedor
from .forms import ProveedorCreationForm, ProveedorUpdateForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin


#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Detalle proveedores'''
class ProveedorDetailView(LoginRequiredMixin, DetailView,PermissionRequiredMixin):
    model = Proveedor
    template_name = 'proveedor/proveedor_detail.html'
    context_object_name = 'proveedor'
    login_url = reverse_lazy('accounts:login')
    permission_required = 'proveedor.ver_proveedor'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Listar proveedores - Uso exclusivo de administrador'''
class ProveedorListView(LoginRequiredMixin,ListView,PermissionRequiredMixin):
    model = Proveedor
    login_url = 'accounts:login'
    template_name = 'proveedor/listar_proveedor.html'
    context_object_name = 'proveedor'
    paginate_by = 5
    permission_required = 'proveedor.ver_proveedor'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Crear proveedores - Uso exclusivo de administrador'''
class ProveedorCreateView(LoginRequiredMixin,CreateView,PermissionRequiredMixin):
    model = Proveedor
    login_url = 'accounts:login'
    template_name = 'proveedor/registro.html'
    form_class = ProveedorCreationForm
    success_url = reverse_lazy('proveedor:lista_proveedor')
    permission_required = 'proveedor.crear_proveedor'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
       

    def form_valid(self, form):
        rut_empresa = form.cleaned_data['rut_empresa']
        proveedor = form.save(commit=False)
        proveedor.rut_empresa = rut_empresa
        proveedor.save()
        messages.success(self.request, "El proveedor se ha registrado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar al proveedor.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Actualizar proveedores - Uso exclusivo de administrador'''
class ProveedorUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin):
    model = Proveedor
    login_url = 'accounts:login'
    template_name = 'proveedor/registro.html'
    form_class = ProveedorUpdateForm
    success_url = reverse_lazy('proveedor:lista_proveedor')
    permission_required = 'proveedor.modificar_proveedor'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["nombre_empresa"].disabled = True
            form.fields["rut_empresa"].disabled = True
        return form
    
    def form_valid(self, form):
        rut_empresa = form.cleaned_data['rut_empresa']
        proveedor = form.save(commit=False)
        proveedor.rut_empresa = rut_empresa
        proveedor.save()
        messages.success(self.request, "El proveedor se ha modificado correctamente")
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al modificar al proveedor.')
        return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Eliminar proveedores - Uso exclusivo de administrador'''
class ProveedorDeleteView(DeleteView,PermissionRequiredMixin):
    model = Proveedor
    login_url = 'accounts:login'
    success_url = reverse_lazy('proveedor:lista_proveedor')
    permission_required = 'proveedor.eliminar_proveedor'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    def form_valid(self, form):
        messages.success(self.request, 'Proveedor eliminado.')
        return super().form_valid(form)

  
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion Buscar proveedores - Uso exclusivo de administrador/recepcionista'''
def buscar_proveedor(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese un término de búsqueda."
        return render(request, 'proveedor/listar_proveedor.html', {'mensaje': mensaje})
    else:
        # Dividir la consulta en palabras individuales
        palabras_clave = query.split()

        # Crear una lista de condiciones OR para cada palabra clave
        condiciones = [Q(nombre_empresa__icontains=palabra) | Q(rut_empresa__icontains=palabra) for palabra in palabras_clave]

        # Combinar las condiciones con OR utilizando el operador '|'
        query_condicion = condiciones.pop()
        for condicion in condiciones:
            query_condicion |= condicion

        # Aplicar la búsqueda utilizando las condiciones construidas
        resultados = Proveedor.objects.filter(query_condicion)

        return render(request, 'proveedor/listar_proveedor.html', {'object_list': resultados})

#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para recargar lista de proveedores - Uso exclusivo de administrador/recepcionista'''
def recargar_proveedor(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/listar_proveedor.html', {'object_list': proveedores})
#------------------------------------------------------------------------------------------------------------------------------#



