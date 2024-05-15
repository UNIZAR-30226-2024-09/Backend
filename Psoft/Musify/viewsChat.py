from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Usuario, Seguido, Seguidor, Cancion, Podcast, Capitulo, Playlist, Colabora, Contiene, Historial, Cola, Genero, Album, Artista, CustomToken, Presentador
from . import DAOs, DAOsChat
from Psoft.serializers import UsuarioSerializer, CancionSerializer, SeguidoSerializer, SeguidorSerializer, PlaylistSerializer, HistorialSerializer, ColaSerializer, CapituloSerializer, PodcastSerializer, AlbumSerializer, ArtistaSerializer, PresentadorSerializer,EstadoSerializer, MensajeSerializer, SalaSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backends import CorreoBackend
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#CORREOS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#Spotify
from dotenv import load_dotenv
import base64
import os
from requests import get, post
import json


class CargarMensajesAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'salaid': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id de la sala'),
        }
    ))
    def post(self, request):
        salaid = request.data['salaid']
        sala = DAOsChat.obtenerSala(salaid)
        if sala is not None:
            mensajes = DAOsChat.cargarMensajes(sala)
            if mensajes is None:
                return Response("No hay mensajes en la sala", status=status.HTTP_200_OK)
            serializer = MensajeSerializer(mensajes, many=True)
            return Response({serializer.data}, status=status.HTTP_200_OK)
        return Response("No existe la sala", status=status.HTTP_404_NOT_FOUND)
    
class RegistrarMensajeAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'salaid': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id de la sala'),
            'emisorid': openapi.Schema(type=openapi.TYPE_STRING, description='Id del emisor'),
            'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje a enviar'),
        }
    ))
    def post(self, request):
        salaid = request.data['salaid']
        sala = DAOsChat.obtenerSala(salaid)
        if sala is not None:
            emisorid = request.data['emisorid']
            emisor = DAOs.conseguirUsuarioPorCorreo(emisorid)
            if emisor is not None:
                mensaje = request.data['mensaje']
                DAOsChat.registrarMensaje(sala, emisor, mensaje)
                return Response("Mensaje registrado", status=status.HTTP_200_OK)
            return Response("No existe el emisor", status=status.HTTP_404_NOT_FOUND)
        return Response("No existe la sala", status=status.HTTP_404_NOT_FOUND)
    
class CrearSalaAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la sala'),
        }
    ))
    def post(self, request):
        nombre = request.data['nombre']
        DAOsChat.crearSala(nombre)
        return Response("Sala creada", status=status.HTTP_200_OK)
    
class BorrarSalaAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'salaid': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id de la sala'),
        }
    ))
    def post(self, request):
        salaid = request.data['salaid']
        sala = DAOsChat.obtenerSala(salaid)
        if sala is not None:
            sala.delete()
            return Response("Sala eliminada", status=status.HTTP_200_OK)
        return Response("No existe la sala", status=status.HTTP_404_NOT_FOUND)
    
class ListarSalasAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        salas = DAOsChat.obtenerSalas()
        if salas is None:
            return Response("No hay salas", status=status.HTTP_200_OK)
        else:
            serializer = SalaSerializer(salas, many=True)
            return Response({'salas': serializer.data}, status=status.HTTP_200_OK)