from django.contrib.auth.backends import ModelBackend as BaseBackend
from .models import User

'''
Clase personalizada de backend de autenticación 

Está verificando si el username proporcionado por el usuario es un correo electrónico 
en lugar de un nombre de usuario. Si el correo electrónico existe en la base de datos,
 entonces la contraseña ingresada se verifica usando el método check_password proporcionado 
 por Django y si la contraseña es correcta, se devuelve el objeto User.

'''

class ModelBackend(BaseBackend):
    def authenticate(self,request, username=None, password=None):
        if not username is None:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass






