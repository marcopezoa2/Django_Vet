
from django.shortcuts import render

# Funcion pagina not found 404
def not_found(request, *args, **kwargs):
    return render(request, 'base/not_found.html', status=404)