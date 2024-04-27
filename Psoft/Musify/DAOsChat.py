from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection  # Assuming you're using Django

def obtenerSalas():
    return models.Sala.objects.all()

def crearSala(nombre):
    models.Sala.objects.create(nombre=nombre)

def obtenerSala(id):
    try:
        return models.Sala.objects.get(id=id)
    except ObjectDoesNotExist:
        return None
    
def cargarMensajes(sala):
    return models.Mensaje.objects.filter(miSala=sala)

def registrarMensaje(sala, usuario, mensaje):
    models.Mensaje.objects.create(miSala=sala, miUsuario=usuario, texto=mensaje)