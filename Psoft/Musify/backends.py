from django.contrib.auth.backends import ModelBackend
from .models import Usuario
from . import DAOs

class CorreoBackend(ModelBackend):
    def authenticate(self, request, correo=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(correo=correo)
            if DAOs.check_user_password(correo,password):
                return user
        except Usuario.DoesNotExist:
            return None
