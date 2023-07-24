from django.http import HttpResponseRedirect
from .models import Producto,RegistroUsoProducto
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import FormView
from .forms import ProductoCreationForm, ProductoUpdateForm, ConsumoProductoForm
from django.db import connection
from django.contrib.auth.mixins import PermissionRequiredMixin


#------------------------------------------------------------------------------------------------------------------------------#

class ProductoDetailView(LoginRequiredMixin, DetailView,PermissionRequiredMixin):
    model = Producto
    template_name = 'inventario/producto_detail.html'
    context_object_name = 'producto'
    login_url = reverse_lazy('accounts:login')

#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Ver productos insumos inventarios - Uso exclusivo de administrador/veterinario'''
'''
class ProductoListView(ListView):
    model = Producto
    login_url = 'accounts:login'
    template_name = 'inventario/listar_producto.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = context['productos']
        productos_alerta = []  # Almacena los productos que requieren una alerta

        # Verificar el stock mínimo de cada producto
        for producto in productos:
            if producto.cantidad <= producto.stock_minimo:
                productos_alerta.append(producto)

        # Enviar una única alerta al administrador por correo electrónico
        if productos_alerta:
            subject = 'Alerta de Stock Mínimo'
            message = 'Estimado administrador,\n\nLos siguientes productos han alcanzado o bajado del stock mínimo:\n\n'
            for producto in productos_alerta:
                message += f'* {producto.nombre} [ stock actual: {producto.cantidad} ]\n'
            message += '\nAtte. ClinicaVet El Valle'

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

        return context

'''

class ProductoListView(ListView,PermissionRequiredMixin):
    model = Producto
    login_url = 'accounts:login'
    template_name = 'inventario/listar_producto.html'
    context_object_name = 'productos'
    paginate_by = 10
    permission_required = 'inventario.ver_producto'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = context['productos']
        productos_alerta = []  # Almacena los productos que requieren una alerta

        # Verificar el stock mínimo de cada producto
        for producto in productos:
            if producto.cantidad <= producto.stock_minimo:
                productos_alerta.append(producto)

        # Enviar una única alerta al administrador por correo electrónico
        if productos_alerta:
            subject = 'Alerta de Stock Mínimo'
            message = 'Estimado administrador,\n\nLos siguientes productos han alcanzado o bajado del stock mínimo:\n\n'
            for producto in productos_alerta:
                message += f'* {producto.nombre} [ stock actual: {producto.cantidad} ]\n'
            message += '\nAtte. ClinicaVet El Valle'

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

        # Llamar al procedimiento almacenado SP_LISTAR_PRODUCTOS
        with connection.cursor() as cursor:
            cursor.callproc("SP_LISTAR_PRODUCTOS")
            cursor.execute("COMMIT")
        
        # Obtener los productos actualizados después de ejecutar el procedimiento almacenado
        productos = Producto.objects.all()
        
        context['productos'] = productos
        return context
    
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase para consumir productos insumos del inventario - Uso exclusivo de administrador/veterinario'''

class ConsumoProductoView(FormView,PermissionRequiredMixin):
    template_name = 'inventario/consumo_producto.html'
    form_class = ConsumoProductoForm
    success_url = reverse_lazy('inventario:lista_producto')
    permission_required = 'inventario.ver_consumoProducto'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    
    # En este caso, se muestra el mensaje de éxito solo si la cantidad utilizada es mayor que el stock mínimo. Si la cantidad utilizada es igual o menor al stock mínimo, solo se muestra el mensaje de advertencia y descuenta el stock.
    
    def form_valid(self, form):
        producto_id = form.cleaned_data['producto_id']
        cantidad_utilizada = form.cleaned_data['cantidad_utilizada']

        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            messages.error(self.request, 'El producto seleccionado no existe.')
            return super().form_invalid(form)

        if cantidad_utilizada <= 0:
            messages.error(self.request, 'La cantidad utilizada debe ser mayor que 0.')
            return super().form_invalid(form)

        if cantidad_utilizada > producto.cantidad:
            messages.error(self.request, 'La cantidad utilizada es mayor que la cantidad disponible en el inventario.')
            return super().form_invalid(form)

        producto.cantidad -= cantidad_utilizada
        producto.save()

        RegistroUsoProducto.objects.create(producto_utilizado=producto, cantidad_utilizada=cantidad_utilizada)

        if producto.cantidad <= producto.stock_minimo:
            messages.warning(self.request, f'El producto {producto.nombre} ha alcanzado o bajado del stock mínimo. Por favor, reponga el producto.')
        else:
            messages.success(self.request, f'Se ha registrado el consumo de {cantidad_utilizada} unidades del producto {producto.nombre}.')

        return super().form_valid(form)
    
'''
class ConsumoProductoView(FormView):
    template_name = 'inventario/consumo_producto.html'
    form_class = ConsumoProductoForm
    success_url = reverse_lazy('inventario:lista_producto')

    def form_valid(self, form):
        producto_id = form.cleaned_data['producto_id']
        cantidad_utilizada = form.cleaned_data['cantidad_utilizada']

        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            messages.error(self.request, 'El producto seleccionado no existe.')
            return super().form_invalid(form)

        if cantidad_utilizada <= 0:
            messages.error(self.request, 'La cantidad utilizada debe ser mayor que 0.')
            return super().form_invalid(form)

        if cantidad_utilizada > producto.cantidad:
            messages.error(self.request, 'La cantidad utilizada es mayor que la cantidad disponible en el inventario.')
            return super().form_invalid(form)

        # Llamar al procedimiento almacenado SP_CONSUMIR_PRODUCTO
        with connection.cursor() as cursor:
            cursor.callproc("SP_CONSUMIR_PRODUCTO", [producto_id, cantidad_utilizada])
            cursor.execute("COMMIT")

        messages.success(self.request, f'Se ha registrado el consumo de {cantidad_utilizada} unidades del producto {producto.nombre}.')

        return super().form_valid(form)
'''
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Crear productos insumos en inventario - Uso exclusivo de administrador'''
class ProductoCreateView(LoginRequiredMixin,CreateView,PermissionRequiredMixin):
    model = Producto
    login_url = 'accounts:login'
    template_name = 'inventario/registro.html'
    form_class = ProductoCreationForm
    success_url = reverse_lazy('inventario:lista_producto')
    permission_required = 'inventario.crear_producto'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields['nombre'].widget.attrs.update({'placeholder': 'Nombre del producto'})
    #     form.fields['descripcion'].widget.attrs.update({'placeholder': 'Descripción'})
    #     form.fields['categoria'].widget.attrs.update({'placeholder': 'Categoria'})
    #     form.fields['proveedor'].widget.attrs.update({'placeholder': 'Proveedor'})
    #     form.fields['cantidad'].widget.attrs.update({'placeholder': 'Cantidad'})
    #     form.fields['stock_minimo'].widget.attrs.update({'placeholder': 'Stock Mínimo'})
    #     form.fields['precio_venta'].widget.attrs.update({'placeholder': 'Precio venta'})
    #     form.fields['precio_compra'].widget.attrs.update({'placeholder': 'Precio compra'})
    #     form.fields['imagen'].widget.attrs.update({'placeholder': 'Imagen'})
    #     for field in form.fields:
    #         form.fields[field].widget.attrs.update({'class': 'form-control'})
    #     return form
    
    def form_valid(self, form):
        messages.success(self.request, 'El producto o insumo se ha registrado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar el producto.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Actualizar productos insumos del inventario - Uso exclusivo de administrador'''
class ProductoUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin):
    model = Producto
    login_url = 'accounts:login'
    template_name = 'inventario/registro.html'
    form_class = ProductoUpdateForm
    success_url = reverse_lazy('inventario:lista_producto')
    permission_required = 'inventario.modificar_producto'

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
        messages.success(self.request, 'El producto o insumo se ha modificado correctamente.')
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al modificar el producto.')
        return super().form_invalid(form)
#------------------------------------------------------------------------------------------------------------------------------#
'''Clase Eliminar productos insumos del inventario - Uso exclusivo de administrador'''
class ProductoDeleteView(DeleteView,PermissionRequiredMixin):
    model = Producto
    login_url = 'accounts:login'
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('inventario:lista_producto')
    permission_required = 'inventario.eliminar_producto'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission_required):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, "¡Producto eliminado con éxito!")
        return reverse_lazy('inventario:lista_producto')


#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion Buscar productos insumos del inventario - Uso exclusivo de administrador/veterinario'''  
def buscar_producto(request):
    query = request.GET.get('q')
    if not query:
        mensaje = "Por favor ingrese un término de búsqueda."
        return render(request, 'inventario/listar_producto.html', {'mensaje': mensaje})
    else:
        # Dividir la consulta en palabras individuales
        palabras_clave = query.split()

        # Crear una lista de condiciones OR para cada palabra clave
        condiciones = [Q(nombre__icontains=palabra) | Q(categoria__nombre__icontains=palabra) | Q(proveedor__nombre_empresa__icontains=palabra) for palabra in palabras_clave]

        # Combinar las condiciones con OR utilizando el operador '|'
        query_condicion = condiciones.pop()
        for condicion in condiciones:
            query_condicion |= condicion

        # Aplicar la búsqueda utilizando las condiciones construidas
        resultados = Producto.objects.filter(query_condicion)

        return render(request, 'inventario/listar_producto.html', {'object_list': resultados})
#------------------------------------------------------------------------------------------------------------------------------#
'''Funcion para recargar lista de productos insumos del inventario - Uso exclusivo de administrador/veterinario'''
def recargar_producto(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/listar_producto.html', {'object_list': productos})
#------------------------------------------------------------------------------------------------------------------------------#














