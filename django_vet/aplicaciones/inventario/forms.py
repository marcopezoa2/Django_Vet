from django import forms
from .models import Producto, RegistroUsoProducto

#------------------------------------------------------------------------------------------------------------------------------#
# fields = ['nombre','descripcion','categoria','proveedor','cantidad','stock_minimo','precio_venta','precio_compra','imagen']
#------------------------------------------------------------------------------------------------------------------------------#
class ProductoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].empty_label = '--- Seleccione un proveedor ---'
        self.fields['categoria'].empty_label = '--- Seleccione una categoria ---'

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','categoria','proveedor','cantidad','stock_minimo','precio_venta','precio_compra','imagen']
        widgets = {
    
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto o insumo'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Ingrese la descripción del producto', 'rows':4}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Ingrese el stock actual'}),
            'stock_minimo': forms.NumberInput(attrs={'placeholder': 'Ingrese el stock mínimo'}),
            'precio_venta': forms.NumberInput(attrs={'placeholder': 'Ingrese el precio de venta del producto o insumo'}),
            'precio_compra': forms.NumberInput(attrs={'placeholder': 'Ingrese el precio de compra del producto o insumo'}),
            'imagen': forms.ClearableFileInput(),
        }
        labels = {
            'nombre' : 'Nombre producto o insumo * ',
            'descripcion': 'Descripción producto o insumo (opcional)',
            'cantidad':  'Stock disponible  *',
            'stock_minimo':  'Stock mínimo *',
            'precio_venta':  'Precio de venta *',
            'precio_compra':'Precio de compra *',
            'proveedor':'Proveedor *',
            'categoria':'Categoria del producto *',
            'imagen':'Imagen producto (opcional)',
        }
#------------------------------------------------------------------------------------------------------------------------------#
class ProductoCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].empty_label = '--- Seleccione un proveedor ---'
        self.fields['categoria'].empty_label = '--- Seleccione una categoria ---'

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','categoria','proveedor','cantidad','stock_minimo','precio_venta','precio_compra','imagen']
        widgets = {
    
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto o insumo'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Ingrese la descripción del producto', 'rows':4}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Ingrese el stock actual'}),
            'stock_minimo': forms.NumberInput(attrs={'placeholder': 'Ingrese el stock mínimo'}),
            'precio_venta': forms.NumberInput(attrs={'placeholder': 'Ingrese el precio de venta del producto o insumo'}),
            'precio_compra': forms.NumberInput(attrs={'placeholder': 'Ingrese el precio de compra del producto o insumo'}),
            'imagen': forms.ClearableFileInput(),
        }
        labels = {
            'nombre' : 'Nombre producto o insumo * ',
            'descripcion': 'Descripción producto o insumo (opcional)',
            'cantidad':  'Stock disponible  *',
            'stock_minimo':  'Stock mínimo *',
            'precio_venta':  'Precio de venta *',
            'precio_compra':'Precio de compra *',
            'proveedor':'Proveedor *',
            'categoria':'Categoria del producto *',
            'imagen':'Imagen producto (opcional)',
        }
#------------------------------------------------------------------------------------------------------------------------------#
class RegistroUsoProductoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto_utilizado'].empty_label = '--- Seleccione un producto ---'

    class Meta:
        model = RegistroUsoProducto
        fields = ['producto_utilizado','cantidad_utilizada']
        labels = {
            'producto_utilizado' : 'Producto utilizado ',
            'cantidad_utilizada': 'Cantidad utilizada',
        }
#------------------------------------------------------------------------------------------------------------------------------#
class ConsumoProductoForm(forms.Form):
    producto_id = forms.IntegerField(label='Producto')
    cantidad_utilizada = forms.IntegerField(label='Cantidad utilizada')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto_id'].empty_label = '--- Seleccione un producto ---'
        self.fields['producto_id'].widget = forms.Select(choices=self.get_productos_choices())

    def get_productos_choices(self):
        productos = Producto.objects.all()
        choices = [(producto.id, producto.nombre) for producto in productos]
        return choices
#------------------------------------------------------------------------------------------------------------------------------#