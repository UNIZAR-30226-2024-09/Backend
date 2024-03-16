from django.contrib.auth.backends import ModelBackend
from .models import Usuario
from . import DAOs

class CorreoBackend(ModelBackend):
    def authenticate(self, request, correo=None, password=None, **kwargs):
        print(f"Intentando autenticar al usuario con correo: {correo}")  # Imprime el correo recibido
        try:
            user = Usuario.objects.get(correo=correo)
            print(f"Usuario encontrado: {user}")  # Imprime el usuario encontrado
            if DAOs.comprobarContrasegna(correo, password):
                print("La contraseña es correcta, autenticación exitosa.")  # Imprime si la contraseña es correcta
                return user
            else:
                print("La contraseña es incorrecta.")  # Imprime si la contraseña es incorrecta
        except Usuario.DoesNotExist:
            print("No existe un usuario con ese correo.")  # Imprime si el usuario no existe
            return None
