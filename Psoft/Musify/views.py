from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Usuario, Seguido, Seguidor, Cancion, Podcast, Capitulo, Playlist, Colabora, Contiene, Historial, Cola, Genero, PertenecenPodcast, PertenecenCancion, Album, Artista, CustomToken, Presentador
from . import DAOs
from Psoft.serializers import UsuarioSerializer, CancionSerializer, SeguidoSerializer, SeguidorSerializer, PlaylistSerializer, HistorialSerializer, ColaSerializer, CapituloSerializer, PodcastSerializer, AlbumSerializer, ArtistaSerializer, PresentadorSerializer,EstadoSerializer, GeneroSerializer, CancionSinAudioSerializer
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
import random
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
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
#def get_token(): #Sacado de tutorial, deberia funcionar
#    auth_string = client_id + ":" + client_secret
#    auth_bytes = auth_string.encode('utf-8')
#    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

#    url='https://accounts.spotify.com/api/token'
#    headers = {
#        'Authorization': 'Basic ' + auth_base64,
#        'Content-Type': 'application/x-www-form-urlencoded'
#    }
#    data = {"grant_type": 'client_credentials'}
#    result = post(url, headers=headers, data=data)
#    json_result = json.loads(result.text)
#    token = json_result['access_token']
#    return token
#token = get_token()
#def get_auth_header(token):
#    return {'Authorization': 'Bearer ' + token}
# VISTAS DE PRUEBA
# GOOGLE
def home(request):
    return render(request, 'home.html')

def lougout_view(request):
    logout(request)
    return redirect("/")

#Enviar correo reporte
def MandarCorreo(receiver,mensaje,subject=""):
    sender = os.getenv("CORREO")
    password = os.getenv("PASSWD_CORREO")
    print(sender)
    print(password)
    # Configurar el servidor de correo
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(mensaje, 'plain'))

    # Enviar el correo
    smtplib.SMTP.debuglevel = 1
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Start TLS encryption
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
        
class ReporteAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'mensaje'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje del usuario')
            },
        ),
        responses={200: 'OK - Reporte enviado con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        mensaje = request.data.get('mensaje')
        MandarCorreo(correo,mensaje,subject="Copia de Reporte Musify")
        return Response({'message': 'Reporte enviado con éxito'}, status=status.HTTP_200_OK)
    
def CorreoRegistro(correo):
    mensaje = "Su registro se ha efectuado con exito, gracias por unirse a Musify"
    MandarCorreo(correo,mensaje,subject="Registro Musify")   
# CORREO DE VERIFICACIÓN
class image_cancion(APIView):
    permission_classes = [AllowAny]
    def get(self, request, filename):
        # Path to the directory where images are stored
        images_dir = 'image_cancion/'

        # Construct the path to the requested image file
        filename += '.jpg'
        image_path = os.path.join(os.path.dirname(__file__),images_dir, filename)
        print(image_path)

        # Check if the file exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                # Read the image content
                image_data = f.read()

                # Determine the content type based on the file extension
                content_type = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'

                # Return the image as an HTTP response
                return HttpResponse(image_data, content_type=content_type)
        else:
            # Return a 404 response if the file does not exist
            return HttpResponse('Image not found', status=404)
        
class image_album(APIView):
    permission_classes = [AllowAny]
    def get(self, request, filename):
        # Path to the directory where images are stored
        images_dir = 'image_album/'

        # Construct the path to the requested image file
        filename += '.jpg'
        image_path = os.path.join(os.path.dirname(__file__),images_dir, filename)
        print(image_path)

        # Check if the file exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                # Read the image content
                image_data = f.read()

                # Determine the content type based on the file extension
                content_type = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'

                # Return the image as an HTTP response
                return HttpResponse(image_data, content_type=content_type)
        else:
            # Return a 404 response if the file does not exist
            return HttpResponse('Image not found', status=404)

class image_artista(APIView):
    permission_classes = [AllowAny]
    def get(self, request, filename):
        # Path to the directory where images are stored
        images_dir = 'image_artista/'

        # Construct the path to the requested image file
        filename += '.jpg'
        image_path = os.path.join(os.path.dirname(__file__),images_dir, filename)
        print(image_path)

        # Check if the file exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                # Read the image content
                image_data = f.read()

                # Determine the content type based on the file extension
                content_type = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'

                # Return the image as an HTTP response
                return HttpResponse(image_data, content_type=content_type)
        else:
            # Return a 404 response if the file does not exist
            return HttpResponse('Image not found', status=404)
        
class image_podcast(APIView):
    permission_classes = [AllowAny]
    def get(self, request, filename):
        # Path to the directory where images are stored
        images_dir = 'image_podcast/'

        # Construct the path to the requested image file
        filename += '.jpg'
        image_path = os.path.join(os.path.dirname(__file__),images_dir, filename)
        print(image_path)

        # Check if the file exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                # Read the image content
                image_data = f.read()

                # Determine the content type based on the file extension
                content_type = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'

                # Return the image as an HTTP response
                return HttpResponse(image_data, content_type=content_type)
        else:
            # Return a 404 response if the file does not exist
            return HttpResponse('Image not found', status=404)

class image_presentador(APIView):
    permission_classes = [AllowAny]
    def get(self, request, filename):
        # Path to the directory where images are stored
        images_dir = 'image_presentador/'

        # Construct the path to the requested image file
        filename += '.jpg'
        image_path = os.path.join(os.path.dirname(__file__),images_dir, filename)
        print(image_path)

        # Check if the file exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                # Read the image content
                image_data = f.read()

                # Determine the content type based on the file extension
                content_type = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'

                # Return the image as an HTTP response
                return HttpResponse(image_data, content_type=content_type)
        else:
            # Return a 404 response if the file does not exist
            return HttpResponse('Image not found', status=404)



class UserViewSet(viewsets.ModelViewSet): #funciona
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


        
'''EJEMPLO DE FORMATO JSON PARA INICIAR SESION
{
    "correo": "john.doe@example.com",
    "contrasegna": "5U3rP@55w0rd"
}
'''

class IniciarSesionAPI(APIView): #Utiliza formato json estandar(el de arriba) funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'contrasegna'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'contrasegna': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario')
            },
        ),
        responses={200: 'OK - Inicio de sesión correcto'}
    )
    def post(self, request):
        
        correo = request.data.get('correo')
        contrasegna = request.data.get('contrasegna')

        # Autenticar al usuario
        usuario = CorreoBackend.authenticate(correo=correo, contrasegna=contrasegna)

        # para el envío de correo de verificación
        #if not usuario.is_email_verified:
        #    return Response({'error': 'Correo no verificado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if usuario is not None:
            # El usuario ha sido autenticado, devolver respuesta de éxito
            token, created = CustomToken.objects.get_or_create(usuario=usuario)
            if created:
                token.save()
            return Response({'message': 'Inicio de sesión correcto',"token": token.key}, status=status.HTTP_200_OK)
        else:
            # El usuario no ha sido autenticado, devolver respuesta de error
            return Response({'error': 'Correo o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)

class CerrarSesionAPI(APIView): 
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get('token')
        token = CustomToken.objects.get(key=token)
        token.delete()
        return Response({'message': 'Cierre de sesión correcto'}, status=status.HTTP_200_OK)
    
class ObtenerUsuarioSesionAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['token'],
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Token del usuario')
            },
        ),
        responses={200: 'OK - Usuario obtenido con éxito'}
    )
    def post(self, request):
        token = request.data.get('token')
        token = CustomToken.objects.get(key=token)
        usuario = token.usuario
        return Response({'correo': usuario.correo, 'nombre': usuario.nombre, 'sexo': usuario.sexo, 'nacimiento': usuario.nacimiento, 'pais': usuario.pais}, status=status.HTTP_200_OK)
'''
class IniciarSesionConGoogleAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Verifica si el usuario ya está autenticado
        if request.user.is_authenticated:
            return redirect('home')  # Redirige al usuario a la página principal si ya está autenticado

        # URL de redireccionamiento después de la autenticación exitosa
        redirect_uri = request.build_absolute_uri('/google/callback')

        # URL de autorización de Google
        auth_uri = 'https://accounts.google.com/o/oauth2/auth'
        # Configura los parámetros de la solicitud de autenticación
        auth_params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'scope': 'email profile openid',
            'response_type': 'code'
        }
        # Genera la URL de autorización de Google
        auth_url = '{}?{}'.format(auth_uri, urllib.parse.urlencode(auth_params))

        return redirect(auth_url)

class GoogleCallbackAPI(APIView):
    permission_classes = [AllowAny]
    def google_callback(request):
        # Obtiene el código de autorización de la solicitud
        code = request.GET.get('code')

        # Intercambia el código de autorización por un token de acceso
        token_url = 'https://oauth2.googleapis.com/token'
        token_params = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': request.build_absolute_uri('/google/callback'),
            'grant_type': 'authorization_code'
        }
        response = requests.post(token_url, data=token_params)

        # Obtiene el token de acceso y verifica su validez
        if response.status_code == 200:
            token_info = response.json()
            id_token.verify_oauth2_token(token_info['id_token'], requests.Request(), settings.GOOGLE_CLIENT_ID)

            # El token es válido, autentica al usuario y redirige a la página principal
            # Aquí debes implementar la lógica para crear o autenticar al usuario en tu sistema
            # Por ejemplo:
            # user = authenticate(request, google_token=token_info['id_token'])
            # login(request, user)
            return redirect('home')
        else:
            # Error al obtener el token de acceso, redirige a una página de error
            return redirect('error')
'''
'''EJEMPLO DE FORMATO JSON PARA REGISTRO
{
    "correo": "john.doe@example.com",
    "nombre": "John Doe",
    "sexo": "Male",
    "nacimiento": "1985-03-10",
    "contrasegna": "5U3rP@55w0rd",
    "pais": "United States"
}
'''
import logging

logger = logging.getLogger(__name__)
#ESTADO CANCIONES
class ObtenerEstadoCancionesAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={200: 'OK - Estado de canciones obtenido con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        serializer = EstadoSerializer(usuario)
        return Response(serializer.data)

class ActualizarEstadoCancionesAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'cancionID', 'tiempo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'cancionID': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción'),
                'tiempo': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tiempo de la canción')
            },
        ),
        responses={200: 'OK - Estado de canciones actualizado con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        cancionID = request.data.get('cancionID')
        cancionVO = DAOs.conseguirCancionPorId(cancionID)
        tiempo = request.data.get('tiempo')
        DAOs.guardarEstado(correo,cancionVO,tiempo)
        return Response({'message': 'Estado de canciones actualizado con éxito'}, status=status.HTTP_200_OK)

class RegistroAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'nombre', 'sexo', 'nacimiento', 'contrasegna', 'pais'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                'sexo': openapi.Schema(type=openapi.TYPE_STRING, description='Sexo del usuario'),
                'nacimiento': openapi.Schema(type=openapi.TYPE_STRING, description='Fecha de nacimiento del usuario'),
                'contrasegna': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
                'pais': openapi.Schema(type=openapi.TYPE_STRING, description='País del usuario')
            },
        ),
        responses={200: 'OK - Usuario registrado con éxito'}
    )

    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        sexo = request.data.get('sexo')
        nacimiento = request.data.get('nacimiento')
        contrasegna = request.data.get('contrasegna')
        pais = request.data.get('pais')
        #generos_seleccionados = request.POST.getlist('generos') # no se si es post o data
        #artistas_seleccionados = request.POST.getlist('artistas') # no se si es post o data

        if not nombre:
            return Response({'error': 'Nombre es un campo obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f'Nombre recibido: {nombre}')

        usuario = Usuario(correo=correo, nombre=nombre, sexo=sexo, nacimiento=nacimiento, contrasegna=contrasegna, pais=pais)

        if Usuario.objects.filter(correo=correo).exists():
            return Response({'error': 'El correo introducido ya tiene asociada una cuenta'}, status=status.HTTP_400_BAD_REQUEST)
        #send_activation_email(usuario, request)
        DAOs.crearUsuario(usuario)
        token = CustomToken.objects.create(usuario=usuario)
        token.save()
        CorreoRegistro(correo)
        return Response({'message': 'Usuario registrado con éxito',"token": token.key}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR USUARIO
{
    "correo": "john.doe@example.com",
    "nombre": "John Doe",
    "sexo": "Male",
    "nacimiento": "1985-03-10",
    "contrasegna": "5U3rP@55w0rd",
    "pais": "United States"
}'''


class ActualizarUsuarioAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'nombre', 'sexo', 'nacimiento', 'contrasegna', 'pais'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                'sexo': openapi.Schema(type=openapi.TYPE_STRING, description='Sexo del usuario'),
                'nacimiento': openapi.Schema(type=openapi.TYPE_STRING, description='Fecha de nacimiento del usuario'),
                'contrasegna': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
                'pais': openapi.Schema(type=openapi.TYPE_STRING, description='País del usuario')
            },
        ),
        responses={
            200: 'OK - Usuario actualizado con éxito',
            }
    )
    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        sexo = request.data.get('sexo')
        nacimiento = request.data.get('nacimiento')
        contrasegna = request.data.get('contrasegna')
        pais = request.data.get('pais')

        # Get the existing user by correo
        try:
            usuario_actual = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            # Handle the case where the user does not exist
            # You may choose to create a new user or return an error response
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Update fields only if they are not null
            if nombre is not None:
                usuario_actual.nombre = nombre
            if sexo is not None:
                usuario_actual.sexo = sexo
            if nacimiento is not None:
                usuario_actual.nacimiento = nacimiento
            if contrasegna is not None:
                usuario_actual.contrasegna = contrasegna
            if pais is not None:
                usuario_actual.pais = pais

            # Save the updated user
            usuario_actual.save()
            return Response({'message': 'Usuario actualizado con éxito'}, status=status.HTTP_200_OK)

'''class ActualizarUsuarioNombreAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'nombre'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario')
            },
        ),
        responses={
            200: 'OK - Nombre de usuario actualizado con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        if not usuario:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            DAOs.actualizarUsuarioNombre(usuario, nombre)
            return Response({'message': 'Nombre de usuario actualizado con éxito'}, status=status.HTTP_200_OK)
    
class ActualizarUsuarioSexoAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'sexo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'sexo': openapi.Schema(type=openapi.TYPE_STRING, description='Sexo del usuario')
            },
        ),
        responses={
            200: 'OK - Sexo de usuario actualizado con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        sexo = request.data.get('sexo')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        if not usuario:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            DAOs.actualizarUsuarioSexo(usuario, sexo)
            return Response({'message': 'Sexo de usuario actualizado con éxito'}, status=status.HTTP_200_OK)
    
class ActualizarUsuarioNacimientoAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'nacimiento'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'nacimiento': openapi.Schema(type=openapi.TYPE_STRING, description='Fecha de nacimiento del usuario')
            },
        ),
        responses={
            200: 'OK - Fecha de nacimiento de usuario actualizada con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        nacimiento = request.data.get('nacimiento')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        DAOs.actualizarUsuarioNacimiento(usuario, nacimiento)
        return Response({'message': 'Fecha de nacimiento de usuario actualizada con éxito'}, status=status.HTTP_200_OK)

class ActualizarUsuarioPaisAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'pais'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'pais': openapi.Schema(type=openapi.TYPE_STRING, description='País del usuario')
            },
        ),
        responses={
            200: 'OK - País de usuario actualizado con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        pais = request.data.get('pais')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        if not usuario:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            DAOs.actualizarUsuarioPais(usuario, pais)
            return Response({'message': 'País de usuario actualizado con éxito'}, status=status.HTTP_200_OK)
        
class ActualizarUsuarioContrasegnaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'contrasegna'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'contrasegna': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario')
            },
        ),
        responses={
            200: 'OK - Contraseña de usuario actualizada con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        contrasegna = request.data.get('contrasegna')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        if not usuario:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            DAOs.actualizarUsuarioContrasegna(usuario, contrasegna)
            return Response({'message': 'Contraseña de usuario actualizada con éxito'}, status=status.HTTP_200_OK)'''
    
'''EJEMPLO DE FORMATO JSON PARA ELIMINAR USUARIO
{
    "correo": "john.doe@example.com"
}
'''
class EliminarUsuarioAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={200: 'OK - Usuario eliminado con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        DAOs.eliminarUsuario(correo)
        return Response({'message': 'Usuario eliminado con éxito'}, status=status.HTTP_200_OK)


'''EJEMPLO DE FORMATO JSON PARA SEGUIR A UN AMIGO
{
    "correo": "john.doe@example.com",
    "amigo": "sarah@gmail.com"
}
'''
#class SeguirAmigoAPI(APIView): # funciona
#    permission_classes = [AllowAny]
#    def post(self, request):
#        correo = request.data.get('correo') # coger el correo de la sesión
#        amigo = request.data.get('amigo') # coger el correo del amigo
#        DAOs.agnadirAmigo(correo, amigo)
#        return Response({'message': 'Amigo añadido con éxito'}, status=status.HTTP_200_OK) 

'''EJEMPLO DE FORMATO JSON PARA SEGUIR A UN USUARIO
{
    "correo": "john.doe@example.com",
    "seguido": "sarah@gmail.com"
}
'''
class SeguirAPI(APIView): # sin comprobar
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'seguido'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'seguido': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario a seguir')
            },
        ),
        responses={
            200: 'OK - Usuario seguido con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        seguido = request.data.get('seguido') # coger el correo del usuario a seguir
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        usuarioSeguir = DAOs.conseguirUsuarioPorCorreo(seguido)
        if not usuarioSeguir or not usuario:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            DAOs.agnadirSeguido(usuario, usuarioSeguir)
            DAOs.agnadirSeguidor(usuarioSeguir, usuario)
            return Response({'message': 'Usuario seguido con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA DEJAR DE SEGUIR A UN USUARIO
{
    "correo": "john.doe@example.com",
    "seguido": "sarah@gmail.com"
}
'''
class DejarDeSeguirAPI(APIView): # sin comprobar
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'seguido'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'seguido': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario a dejar de seguir')
            },
        ),
        responses={
            200: 'OK - Usuario dejado de seguir con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        seguido = request.data.get('seguido')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        usuarioSiguiendo = DAOs.conseguirUsuarioPorCorreo(seguido)
        if not usuarioSiguiendo or not usuario:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            DAOs.eliminarSeguido(usuario, usuarioSiguiendo)
            DAOs.eliminarSeguidor(usuarioSiguiendo, usuario)
            return Response({'message': 'Usuario dejado de seguir con éxito'}, status=status.HTTP_200_OK)


class ListarSeguidosAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={
            200: 'OK - Seguidos listados con éxito'
        }
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        seguidos = DAOs.listarSeguidos(usuario)
        if seguidos:
            serializer = SeguidoSerializer(seguidos, many=True)
            numSeguidos = DAOs.numeroSeguidos(usuario)
            return Response({'seguidos': serializer.data, 'numSeguidos': numSeguidos}, status=status.HTTP_200_OK)
        
        else:
            return Response({'message': 'No sigue a nadie'}, status=status.HTTP_200_OK)   

class ListarSeguidoresAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={200: 'OK - Seguidores listados con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        seguidores = DAOs.listarSeguidores(usuario)
        if seguidores:
            serializer = SeguidorSerializer(seguidores, many=True)
            numSeguidores = DAOs.numeroSeguidores(usuario)
            return Response({'seguidores': serializer.data, 'numSeguidores': numSeguidores}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene seguidores'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR AMIGOS
{
    "correo": "Paco@gmail.com"
}'''
#class ListarAmigosAPI(APIView): # funciona
#    permission_classes = [AllowAny]
#    def post(self, request):
#        correo = request.data.get('correo') # coger el correo de la sesión
#        amigos = DAOs.listarAmigos(correo)
#        if amigos:
#            serializer = AmigosSerializer(amigos, many=True)
#            return Response({'amigos': serializer.data}, status=status.HTTP_200_OK)
#        else:
#            return Response({'message': 'No tiene amigos'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA DEJAR DE SEGUIR A UN AMIGO
{
    "correo": "john.doe@example.com",
    "amigo": "sarah@gmail.com"
}
'''
#class DejarDeSeguirAmigoAPI(APIView): # funciona
#    permission_classes = [AllowAny]
#    def post(self, request):
#        correo = request.data.get('correo') # coger el correo de la sesión
#        amigo = request.data.get('amigo')
#        DAOs.eliminarAmigo(correo, amigo)
#        return Response({'message': 'Amigo eliminado con éxito'}, status=status.HTTP_200_OK)
    
'''EJEMPLO DE FORMATO JSON PARA COMPROBAR SI DOS USUARIOS SON AMIGOS
{
    "correo": "john.doe@example.com",
    "esSeguido": "sarah@gmail.com"
}
'''
class SiguiendoAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'esSeguido'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'esSeguido': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario a comprobar si es amigo')
            },
        ),
        responses={
            200: 'OK - Comprobación de amistad realizada con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        correoAmigo = request.data.get('esSeguido')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        amigo = DAOs.conseguirUsuarioPorCorreo(correoAmigo)
        if not usuario or not amigo:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        if DAOs.siguiendo(usuario, amigo) == True:
            return Response({'siguiendo': True, 'message': 'Está siguiendo al usuario'}, status=status.HTTP_200_OK)
        else:
            return Response({'siguiendo': False, 'message': 'No está siguiendo al usuario'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR UNA PLAYLIST        
{
    "correo": "sarah@gmail.com",
    "nombre": "Playlist de Paco",
    "publica": true
}'''
class CrearPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'nombre', 'publica'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la playlist'),
                'publica': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si la playlist es pública o privada')
            },
        ),
        responses={200: 'OK - Playlist creada con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        publica = request.data.get('publica')
        if Playlist.objects.filter(nombre=nombre).exists():            
            if Colabora.objects.filter(miUsuario=correo, miPlaylist=DAOs.conseguirPlaylistPorNombre(nombre).id).exists():
                    return Response({'error': 'La playlist ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.crearPlaylist(correo, nombre, publica)
            return Response({'message': 'La playlist se ha creado con éxito'}, status=status.HTTP_200_OK)

class CrearPlaylistGeneralAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la playlist')
            },
        ),
        responses={200: 'OK - Playlist creada con éxito'}
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        DAOs.crearPlaylistGeneral(nombre)
        return Response({'message': 'La playlist se ha creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR UNA PLAYLIST
{
    "playlistId": "2",
    "nombre": "Playlist de Sarah",
    "publica": "False"
}'''

class ActualizarPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId', 'nombre', 'publica'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre de la playlist'),
                'publica': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si la playlist es pública o privada')
            },
        ),
        responses={200: 'OK - Playlist actualizada con éxito'}
    )
    def post(self, request):
        playlistId = request.data.get('playlistId')
        nombre = request.data.get('nombre')
        publica = request.data.get('publica')
        playlist = DAOs.conseguirPlaylistPorId(playlistId)
        if playlist is None:
            return Response({'error': 'La playlist no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarPlaylist(playlist, nombre, publica)
            return Response({'message': 'La playlist ha sido actualizada con éxito'}, status=status.HTTP_200_OK)
    
class AñadirColaboradorAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'playlistId'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist')
            },
        ),
        responses={200: 'OK - Colaborador añadido con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        playlistId = request.data.get('playlistId')
        playlist = DAOs.conseguirPlaylistPorId(playlistId)
        if playlist is None:
            return Response({'error': 'La playlist no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.agnadirColaborador(playlist, correo)
            return Response({'message': 'Colaborador añadido con éxito'}, status=status.HTTP_200_OK)

'''class ActualizarPlaylistNombreAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId', 'nombre'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre de la playlist')
            },
        ),
        responses={
            200: 'OK - Nombre de la playlist actualizado con éxito',
            400: 'Bad Request - La playlist no existe'
            }
    )
    def post(self, request):
        playlistId = request.data.get('playlistId')
        nombre = request.data.get('nombre')
        playlist = DAOs.conseguirPlaylistPorId(playlistId)
        if playlist is None:
            return Response({'error': 'La playlist no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarPlaylistNombre(playlist, nombre)
            return Response({'message': 'Nombre de la playlist actualizado con éxito'}, status=status.HTTP_200_OK)
        
class ActualizarPlaylistPublicaAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId', 'publica'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist'),
                'publica': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si la playlist es pública o privada')
            },
        ),
        responses={
            200: 'OK - Privacidad de la playlist actualizada con éxito',
            400: 'Bad Request - La playlist no existe'
            }
    )
    def post(self, request):
        playlistId = request.data.get('playlistId')
        publica = request.data.get('publica')
        playlist = DAOs.conseguirPlaylistPorId(playlistId)
        if playlist is None:
            return Response({'error': 'La playlist no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarPlaylistPublica(playlist, publica)
            return Response({'message': 'Privacidad de la playlist actualizada con éxito'}, status=status.HTTP_200_OK)'''

class ListarCancionesAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Canciones listadas con éxito'}
    )
    def post(self, request):
        canciones = DAOs.listarCanciones()
        canciones #QUITAR EN VERSION FUNCIONAL, HECHO PARA TESTEAR HOY YA QUE NO ESTA DEL TODO TERMINADO
        # Verificar si se encontraron canciones en la playlist
        if canciones:
            serializer = CancionSerializer(canciones, many=True)
            # Devolver la lista de canciones serializadas en formato JSON
            return Response({'canciones': serializer.data}, status=status.HTTP_200_OK)
        else:
            # Si no se encontraron canciones, devolver un mensaje indicando lo mismo
            return Response({'message': 'No hay canciones'}, status=status.HTTP_200_OK)
        
class ListarPocasCancionesAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Canciones listadas con éxito'}
    )
    def post(self, request):
        canciones = DAOs.listarPocasCanciones()
        # Verificar si se encontraron canciones en la playlist
        if canciones:
            serializer = CancionSerializer(canciones, many=True)
            # Devolver la lista de canciones serializadas en formato JSON
            return Response({'canciones': serializer.data}, status=status.HTTP_200_OK)
        else:
            # Si no se encontraron canciones, devolver un mensaje indicando lo mismo
            return Response({'message': 'No hay canciones'}, status=status.HTTP_200_OK)
        
class ListarPocosPodcastsAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Podcasts listados con éxito'}
    )
    def post(self, request):
        podcasts = DAOs.listarPocosPodcasts()
        # Verificar si se encontraron podcasts en la playlist
        if podcasts:
            serializer = PodcastSerializer(podcasts, many=True)
            # Devolver la lista de podcasts serializados en formato JSON
            return Response({'podcasts': serializer.data}, status=status.HTTP_200_OK)
        else:
            # Si no se encontraron podcasts, devolver un mensaje indicando lo mismo
            return Response({'message': 'No hay podcasts'}, status=status.HTTP_200_OK)
        
class getSongByIdAPI(APIView): # No funciona ni para atras
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['cancionId'],
        properties={
            'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la cancion')
        },
        ),
        responses={200: 'OK - Cancion listada con éxito'}
    )
    def post(self, request):
        cancionId = request.data.get('cancionId')
        audio = DAOs.audioDeCancion(cancionId)
        
        if audio is not None:
            return Response({'audio': audio}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No existe'}, status=status.HTTP_200_OK)
        
class ListarPodcastsAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Podcasts listados con éxito'}
    )
    def post(self, request):
        podcasts = DAOs.listarPodcasts()
        # Verificar si se encontraron podcasts en la playlist
        if podcasts:
            serializer = PodcastSerializer(podcasts, many=True)
            # Devolver la lista de podcasts serializados en formato JSON
            return Response({'podcasts': serializer.data}, status=status.HTTP_200_OK)
        else:
            # Si no se encontraron podcasts, devolver un mensaje indicando lo mismo
            return Response({'message': 'No hay podcasts'}, status=status.HTTP_200_OK)


'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS CANCIONES DE UNA PLAYLIST
{
    "correo": "sarah@gmail.com",
    "playlistId": "2"
}'''
class ListarCancionesPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist')
            },
        ),
        responses={200: 'OK - Canciones listadas con éxito'}
    )
    def post(self, request):
        playlistId = request.data.get('playlistId')  # Obtener el ID de la playlist
        canciones = DAOs.listarCancionesPlaylist(playlistId)
        # Verificar si se encontraron canciones en la playlist
        if canciones:
            serializer = CancionSerializer(canciones, many=True)
            # Devolver la lista de canciones serializadas en formato JSON
            return Response({'canciones': serializer.data}, status=status.HTTP_200_OK)
        else:
            # Si no se encontraron canciones, devolver un mensaje indicando lo mismo
            return Response({'message': 'La playlist no tiene canciones'}, status=status.HTTP_200_OK)
        

class ListarPlaylistEnElCocheAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Playlists en el coche listada con éxito'}
    )
    def post(self, request):
        cancionesCoche = DAOs.listarCancionesPlaylist(62)
        if cancionesCoche:
            serializerCoche = CancionSerializer(cancionesCoche, many=True)
            return Response({'canciones': serializerCoche.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay canciones en la playlist en el coche'}, status=status.HTTP_200_OK)
        
class ListarPlaylistEjercicioAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Playlist de ejercicio listada con éxito'}
    )
    def post(self, request):
        cancionesGym = DAOs.listarCancionesPlaylist(63)
        if cancionesGym:
            serializerGym = CancionSerializer(cancionesGym, many=True)
            return Response({'canciones': serializerGym.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay canciones en la playlist de ejercicio'}, status=status.HTTP_200_OK)
        
class ListarPlaylistRelaxAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Playlist de relax listada con éxito'}
    )
    def post(self, request):
        cancionesRelax = DAOs.listarCancionesPlaylist(64)
        if cancionesRelax:
            serializerRelax = CancionSerializer(cancionesRelax, many=True)
            return Response({'canciones': serializerRelax.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay canciones en la playlist de relax'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN A UNA PLAYLIST
{
    "playlistId": "2",
    "cancionId": "26"
}'''

class AgnadirCancionPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId', 'cancionId'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist'),
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Canción añadida con éxito a la playlist',
            400: 'Bad Request - La canción ya está en la playlist'
        }
    )
    def post(self, request):
        #correo = request.data.get('email') # coger correo de la sesión
        playlistId = request.data.get('playlistId')
        cancionId = request.data.get('cancionId')
        if Contiene.objects.filter(miAudio=cancionId, miPlaylist=playlistId).exists():
            return Response({'error': 'La canción ya está en la playlist'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.agnadirCancionPlaylist(playlistId, cancionId)
        return Response({'message': 'La canción ha sido añadida con éxito a la playlist'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ELIMINAR UNA CANCIÓN DE UNA PLAYLIST
{
    "playlistId": "2",
    "cancionId": "26"
}'''

class EliminarCancionPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId', 'cancionId'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist'),
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Canción eliminada con éxito de la playlist',
            400: 'Bad Request - La canción no existe en la playlist'}
    )
    def post(self, request):
        playlistId = request.data.get('playlistId')
        cancionId = request.data.get('cancionId')
        if not Contiene.objects.filter(miAudio=cancionId, miPlaylist=playlistId).exists():
            return Response({'error': 'La canción no existe en la playlist'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.eliminarCancionPlaylist(playlistId, cancionId)
        return Response({'message': 'La canción ha sido eliminada con éxito de la playlist'}, status=status.HTTP_200_OK)
 
'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS PLAYLISTS DE UN USUARIO
{
    "correo": "sarah@gmail.com"
}
'''
class ListarPlaylistsUsuarioAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={200: 'OK - Playlists listadas con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        playlists = DAOs.listarPlaylistsUsuario(correo)
        if playlists:
            serializer = PlaylistSerializer(playlists, many=True)
            return Response({'playlists': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene playlists'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR CANCIÓN
{
    "nombre": "Buenas tardes",
    "nombreFoto": "Homecoming_cover.jpg",
    "miAlbum": "15",
    "nombreArchivoMp3": "Kanye West - Homecoming_LQ488QrqGE4.mp3"
}'''

def convertirBinario(ruta):
    #entre las comillas y antes de las dos barras hay que poner la ruta del archivo, teniendo en cuenta que ruta tiene el nombre del archivo
    with open(r"C:\Users\nerea\Downloads\\" + ruta, "rb") as archivo:
        contenido_binario = archivo.read()
        contenido_base64 = base64.b64encode(contenido_binario)
    return contenido_base64


import base64
from PIL import Image
from io import BytesIO

def save_base64_image(base64_string, output_path):
    try:
        # Decode the Base64 string into bytes
        image_data = base64.b64decode(base64_string)
        
        # Open the image using PIL
        image = Image.open(BytesIO(image_data))
        
        # Save the image as JPG
        image.save(output_path, format='JPEG')
        
        print(f"Image saved successfully to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")


class CrearCancionAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre', 'nombreFoto', 'miAlbum', 'audiofile'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la canción'),
                'imagen_b64': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BASE64, description='Imagen de la canción'),
                'miAlbum': openapi.Schema(type=openapi.TYPE_STRING, description='ID del álbum'),
                'audiofile': openapi.Schema(type=openapi.TYPE_FILE, description='Archivo de audio de la canción')
            },
        ),
        responses={200: 'OK - Canción creada con éxito'}
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        imagen_b64 = request.data.get('imagen_b64')
        miAlbum = request.data.get('miAlbum')
        audiofile = request.data.get('audiofile')

        current_dir = os.getcwd()
        directorio = os.path.join(current_dir, 'Musify/image_cancion/')
        puntuacion = 0 # cuando se crea la canción en nuestra app, se crea con puntuación 0
        numeroPuntuaciones = 0
        audiofile = base64.b64encode(audiofile.read())
        if miAlbum != '':
            miAlbum = DAOs.conseguirAlbumPorId(miAlbum)
        else:
            miAlbum = None
        
        cancion = Cancion(nombre=nombre, miAlbum=miAlbum, puntuacion=puntuacion, numPuntuaciones=numeroPuntuaciones, archivoMp3=audiofile)
        cancion2 = DAOs.crearCancion(cancion)
        path = directorio + str(cancion2.id) + ".jpg"
        save_base64_image(imagen_b64, path)
        return Response({'message': 'Canción creada con éxito'}, status=status.HTTP_200_OK)

class DevolverCancionAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cancionId'],
            properties={
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Canción devuelta con éxito',
            404: 'NOT FOUND - La canción no existe'
        }
    )
    def post(self, request):
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if cancion:
            serializer = CancionSerializer(cancion)
            return Response({'cancion': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'La canción no existe'}, status=status.HTTP_404_NOT_FOUND)

class DevolverAlbumAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['albumId'],
            properties={
                'albumId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del álbum')
            },
        ),
        responses={
            200: 'OK - Álbum devuelto con éxito',
            404: 'NOT FOUND - El álbum no existe'
        }
    )
    def post(self, request):
        albumId = request.data.get('albumId')
        album = DAOs.conseguirAlbumPorId(albumId)
        if album:
            serializer = AlbumSerializer(album)
            return Response({'album': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El álbum no existe'}, status=status.HTTP_404_NOT_FOUND)

class DevolverPlaylistAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist')
            },
        ),
        responses={
            200: 'OK - Playlist devuelta con éxito',
            404: 'NOT FOUND - La playlist no existe'
        }
    )
    def post(self, request):
        playlistId = request.data.get('playlistId')
        playlist = DAOs.conseguirPlaylistPorId(playlistId)
        if playlist:
            serializer = PlaylistSerializer(playlist)
            return Response({'playlist': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'La playlist no existe'}, status=status.HTTP_404_NOT_FOUND)

class DevolverPodcastAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del podcast')
            },
        ),
        responses={
            200: 'OK - Podcast devuelto con éxito',
            404: 'NOT FOUND - El podcast no existe'
        }
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if podcast:
            serializer = PodcastSerializer(podcast)
            return Response({'podcast': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El podcast no existe'}, status=status.HTTP_404_NOT_FOUND)
        
class DevolverCapituloAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['capituloId'],
            properties={
                'capituloId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del capítulo')
            },
        ),
        responses={
            200: 'OK - Capítulo devuelto con éxito',
            404: 'NOT FOUND - El capítulo no existe'
        }
    )
    def post(self, request):
        capituloId = request.data.get('capituloId')
        capitulo = DAOs.conseguirCapituloPorId(capituloId)
        if capitulo:
            serializer = CapituloSerializer(capitulo)
            return Response({'capitulo': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El capítulo no existe'}, status=status.HTTP_404_NOT_FOUND)
        
class DevolverUsuarioAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={
            200: 'OK - Usuario devuelto con éxito',
            404: 'NOT FOUND - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        if usuario:
            serializer = UsuarioSerializer(usuario)
            return Response({'usuario': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        
class DevolverArtistaAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['artistaId'],
            properties={
                'artistaId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del artista')
            },
        ),
        responses={
            200: 'OK - Artista devuelto con éxito',
            404: 'NOT FOUND - El artista no existe'
        }
    )
    def post(self, request):
        artistaId = request.data.get('artistaId')
        artista = DAOs.conseguirArtistaPorId(artistaId)
        if artista:
            serializer = ArtistaSerializer(artista)
            return Response({'artista': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El artista no existe'}, status=status.HTTP_404_NOT_FOUND)
        
class DevolverPresentadorAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['presentadorId'],
            properties={
                'presentadorId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del presentador')
            },
        ),
        responses={
            200: 'OK - Presentador devuelto con éxito',
            404: 'NOT FOUND - El presentador no existe'
        }
    )
    def post(self, request):
        presentadorId = request.data.get('presentadorId')
        presentador = DAOs.conseguirPresentadorPorId(presentadorId)
        if presentador:
            serializer = PresentadorSerializer(presentador)
            return Response({'presentador': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El presentador no existe'}, status=status.HTTP_404_NOT_FOUND)
        

'''EJEMPLO DE FORMATO JSON PARA PUNTUAR UNA CANCIÓN
{}
    "cancionId": "27",
    "puntuacion": "4"
}'''

class PuntuarCancionAPI(APIView): # comprobar
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cancionId', 'puntuacion'],
            properties={
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción'),
                'puntuacion': openapi.Schema(type=openapi.TYPE_INTEGER, description='Puntuación a asignar')
            },
        ),
        responses={200: 'OK - Canción puntuada con éxito'}
    )
    def post(self, request):
        cancionId = request.data.get('cancionId')
        puntuacion = request.data.get('puntuacion')
        puntuacionActual = DAOs.puntuacionCancion('cancionId')
        numeroPuntuaciones = DAOs.numeroPuntuaciones('cancionId')
        puntuacion = (puntuacionActual + puntuacion) / (numeroPuntuaciones + 1)
        DAOs.aumentarNumeroPuntuaciones('cancionId', numeroPuntuaciones + 1)
        DAOs.puntuarCancion(cancionId, puntuacion)
        return Response({'message': 'Canción puntuada con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR O QUITAR UNA CANCION DE FAVORITOS
{
    "correo": "sarah@gmail.com",
    "cancionId": "14",
    "favorito": "True"
}'''
class EditarCancionFavoritosAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'cancionId', 'favorito'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción'),
                'favorito': openapi.Schema(type=openapi.TYPE_STRING, description='True si se quiere añadir a favoritos, False si se quiere eliminar')
            },
        ),
        responses={
            200: 'OK - Canción añadida a favoritos con éxito',
            200: 'OK - Canción eliminada de favoritos con éxito'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        cancionId = request.data.get('cancionId')
        favorito = request.data.get('favorito')
        playlistId = DAOs.favoritoUsuario(correo)
        if favorito == "True":
            DAOs.agnadirCancionPlaylist(playlistId, cancionId)
            return Response({'message': 'Canción añadida a favoritos con éxito'}, status=status.HTTP_200_OK)
        else:
            DAOs.eliminarCancionPlaylist(playlistId, cancionId)
            return Response({'message': 'Canción eliminada de favoritos con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA SABER SI UNA CANCIÓN ESTÁ EN FAVORITOS PARA EL USUARIO
{
    "correo": "prueba@gmail",
    "cancionId": "14",
}'''
class EsFavoritaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'cancionId'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción')
            },
        ),
        responses={200: 'OK - La canción está en favoritos',
                   200: 'NO OK - La canción no está en favoritos'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        cancionId = request.data.get('cancionId')
        cancionVO = DAOs.conseguirCancionPorId(cancionId)
        if cancionVO is not None:
            if DAOs.cancionFavorita(correo, cancionVO):
                return Response({'message': 'True'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'False'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'La canción no existe'}, status=status.HTTP_404_NOT_FOUND)
class EliminarPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['playlistId'],
            properties={
                'playlistId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la playlist')
            },
        ),
        responses={200: 'OK - Playlist eliminada con éxito'}
    )
    def post(self, request):
        playlistId = request.data.get('playlistId')
        DAOs.eliminarPlaylist(playlistId)
        return Response({'message': 'Playlist eliminada con éxito'}, status=status.HTTP_200_OK)
'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN A LA COLA DE REPRODUCCIÓN
{
    "correo": "sarah@gmail.com",
    "cancionId": "27"
}'''

class AgnadirCancionColaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'cancionId'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Canción añadida a la cola de reproducción con éxito',
            400: 'Bad Request - La canción no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if cancion is None:
            return Response({'error': 'La canción no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if DAOs.comprobarCancionCola(correo, cancion) == False:
                DAOs.agnadirCancionCola(correo, cancion)
                return Response({'message': 'Canción añadida a la cola de reproducción con éxito'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'La canción ya está en la cola de reproducción'}, status=status.HTTP_200_OK)

class EliminarCancionColaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'cancionId'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción')
            },
        ),
        responses={200: 'OK - Canción eliminada de la cola de reproducción con éxito',
                   400: 'Bad Request - La canción no existe en la cola de reproducción'}
    )
    def post(self, request):
        correo = request.data.get('correo')
        cancionId = request.data.get('cancionId')
        if not Cola.objects.filter(miUsuario=correo, miAudio=cancionId).exists():
            return Response({'error': 'La canción no existe en la cola de reproducción'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.eliminarCancionCola(correo, cancionId)
        return Response({'message': 'Canción eliminada de la cola de reproducción con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR ÁLBUM
{
    "nombre": "album de Sarah"
}'''

class CrearAlbumAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del álbum')
            },
        ),
        responses={200: 'OK - Álbum creado con éxito'}
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        album = Album(nombre=nombre)
        DAOs.crearAlbum(album)
        return Response({'message': 'Álbum creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR ÁLBUM
{
    "albumId": "1",
    "nombre": "album de Sarah",
    "nombreFoto": "Homecoming_cover.jpg"
}'''
class ActualizarAlbumAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['albumId', 'nombre', 'nombreFoto'],
            properties={
                'albumId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del álbum'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre del álbum'),
                'foto': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la foto')
            },
        ),
        responses={
            200: 'OK - Álbum actualizado con éxito',
            400: 'Bad Request - El álbum no existe'
            }
    )
    def post(self, request):
        albumId = request.data.get('albumId')
        nombre = request.data.get('nombre')
        nombreFoto = request.data.get('nombreFoto')
        album = DAOs.conseguirAlbumPorId(albumId)
        contenidoBinarioFoto = convertirBinario(nombreFoto)
        if album is None:
            return Response({'error': 'El álbum no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarAlbum(album, nombre, contenidoBinarioFoto)
            return Response({'message': 'Álbum actualizado con éxito'}, status=status.HTTP_200_OK)
        
'''class ActualizarAlbumNombreAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['albumId', 'nombre'],
            properties={
                'albumId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del álbum'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre del álbum')
            },
        ),
        responses={
            200: 'OK - Nombre del álbum actualizado con éxito',
            400: 'Bad Request - El álbum no existe'
            }
    )
    def post(self, request):
        albumId = request.data.get('albumId')
        nombre = request.data.get('nombre')
        album = DAOs.conseguirAlbumPorId(albumId)
        if album is None:
            return Response({'error': 'El álbum no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarAlbumNombre(album, nombre)
            return Response({'message': 'Nombre del álbum actualizado con éxito'}, status=status.HTTP_200_OK)

class ActualizarAlbumFotoAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['albumId', 'nombreFoto'],
            properties={
                'albumId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del álbum'),
                'nombreFoto': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la foto')
            },
        ),
        responses={
            200: 'OK - Foto del álbum actualizada con éxito',
            400: 'Bad Request - El álbum no existe'
            }
    )
    def post(self, request):
        albumId = request.data.get('albumId')
        nombreFoto = request.data.get('nombreFoto')
        album = DAOs.conseguirAlbumPorId(albumId)
        if album is None:
            return Response({'error': 'El álbum no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            contenidoBinarioFoto = convertirBinario(nombreFoto)
            DAOs.actualizarAlbumFoto(album, contenidoBinarioFoto)
            return Response({'message': 'Foto del álbum actualizada con éxito'}, status=status.HTTP_200_OK)'''

'''EJEMPLO DE FORMATO JSON PARA CREAR AÑADIR CANCIÓN A UN ÁLBUM
{
    "albumNombre": "album de Sarah",
    "cancionId": "Buenas tardes"
}'''

class AgnadirCancionAlbumAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['albumNombre', 'cancionId'],
            properties={
                'albumNombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del álbum'),
                'cancionId': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la canción')
            },
        ),
        responses={200: 'OK - Canción añadida al álbum con éxito',
                   400: 'Bad Request - La canción ya existe en el álbum'}
    )
    def post(self, request):
        albumNombre = request.data.get('albumNombre')
        album = DAOs.conseguirAlbumPorNombre(albumNombre)
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if album is None or cancion is None:
            return Response({'error': 'El álbum o la canción no existen'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if Cancion.objects.filter(nombre=cancionId, miAlbum=album).exists():
                return Response({'message': 'La cancion ya existe está en el álbum'}, status=status.HTTP_400_BAD_REQUEST)
            DAOs.agnadirCancionAlbum(album, cancion)
            return Response({'message': 'Canción añadida al álbum con éxito'}, status=status.HTTP_200_OK)

class PuntuarPodcastAPI(APIView): #comprobar
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId', 'puntuacion'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast'),
                'puntuacion': openapi.Schema(type=openapi.TYPE_INTEGER, description='Puntuación del podcast')
            },
        ),
        responses={200: 'OK - Podcast puntuada con éxito'}
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        puntuacion = request.data.get('puntuacion')
        puntuacionActual = DAOs.puntuacionPodcast('podcastId')
        numeroPuntuaciones = DAOs.numeroPuntuacionesPodcast('podcastId')
        puntuacion = (puntuacionActual + puntuacion) / (numeroPuntuaciones + 1)
        DAOs.aumentarNumeroPuntuacionesPodcast('podcastId', numeroPuntuaciones + 1)
        DAOs.puntuarPodcast(podcastId, puntuacion)
        return Response({'message': 'Podcast puntuada con éxito'}, status=status.HTTP_200_OK)


'''EJEMPLO DE FORMATO JSON PARA CREAR CAPITULO
{
    "nombre": "episodio1",
    "descripcion": "descripcion del epidodio1",
    "podcastId": "2",
    "nombreArchivoMp3": "archivo.mp3"
}'''

class CrearCapituloAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre', 'descripcion', 'podcastId', 'nombreArchivoMp3'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del capítulo'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del capítulo'),
                'podcastId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast'),
                'nombreArchivoMp3': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del archivo mp3')
            },
        ),
        responses={200: 'OK - Capítulo almacenado correctamente',
                   400: 'Bad Request - El podcast no existe'}
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        podcastId = request.data.get('podcastId')
        nombreArchivoMp3 = request.data.get('nombreArchivoMp3')
        if podcastId != '':
            miPodcast = DAOs.conseguirPodcastPorId(podcastId)
            if miPodcast is not None:
                #contenidoBinarioMp3 = convertirBinario(nombreArchivoMp3)
                capitulo = Capitulo(nombre=nombre, descripcion=descripcion, miPodcast=miPodcast, archivoMp3=nombreArchivoMp3)
                DAOs.crearCapitulo(capitulo)
                return Response({'message': 'Capítulo almacenado correctamente'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)

class ActualizarCancionAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cancionId', 'nombre', 'nombreFoto', 'miAlbum', 'nombreArchivoMp3'],
            properties={
                'cancionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la canción'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre de la canción'),
                'nombreFoto': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la foto'),
                'miAlbum': openapi.Schema(type=openapi.TYPE_STRING, description='ID del álbum'),
                'nombreArchivoMp3': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del archivo mp3')
            },
        ),
        responses={
            200: 'OK - Canción actualizada con éxito',
            400: 'Bad Request - La canción no existe',
            400: 'Bad Request - El álbum no existe'
        }
    )
    def post(self, request):
        cancionId = request.data.get('cancionId')
        nombre = request.data.get('nombre')
        nombreFoto = request.data.get('nombreFoto')
        miAlbum = request.data.get('miAlbum')
        nombreMp3 = request.data.get('nombreArchivoMp3')
        miAlbum = DAOs.conseguirAlbumPorId(miAlbum)
        cancion = DAOs.conseguirCancionPorId(cancionId)
        contenidoBinarioMp3 = convertirBinario(nombreMp3)
        contenidoBinarioFoto = convertirBinario(nombreFoto)
        if cancion is None:
            return Response({'error': 'La canción no existe'}, status=status.HTTP_400_BAD_REQUEST)
        elif miAlbum is None:
            return Response({'error': 'El álbum no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarCancion(cancion, nombre, contenidoBinarioFoto, miAlbum, contenidoBinarioMp3)
            return Response({'message': 'Canción actualizada con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR CAPITULO
{
    "capituloId": "1",
    "nombre": "episodio1",
    "descripcion": "descripcion del epidodio1",
    "miPodcast": "podcast2" 
}'''
class ActualizarCapituloAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['capituloId', 'nombre', 'descripcion', 'miPodcast'],
            properties={
                'capituloId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del capítulo'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre del capítulo'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva descripción del capítulo'),
                'miPodcast': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del podcast')
            },
        ),
        responses={
            200: 'OK - Capítulo actualizado con éxito',
            400: 'Bad Request - El capítulo no existe',
            400: 'Bad Request - El podcast no existe'
        }
    )
    def post(self, request):
        capituloId = request.data.get('capituloId')
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        miPodcast = request.data.get('miPodcast')
        miPodcast = DAOs.conseguirPodcastPorNombre(miPodcast)
        capitulo = DAOs.conseguirCapituloPorId(capituloId)
        if capitulo is None:
            return Response({'error': 'El capítulo no existe'}, status=status.HTTP_400_BAD_REQUEST)
        elif miPodcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarCapitulo(capitulo, nombre, descripcion, miPodcast)
            return Response({'message': 'Capítulo actualizado con éxito'}, status=status.HTTP_200_OK)
        
    
'''class ActualizarCapituloNombreAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['capituloId', 'nombre'],
            properties={
                'capituloId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del capítulo'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre del capítulo')
            },
        ),
        responses={
            200: 'OK - Nombre del capítulo actualizado con éxito',
            400: 'Bad Request - El capítulo no existe'
        }
    )
    def post(self, request):
        capituloId = request.data.get('capituloId')
        nombre = request.data.get('nombre')
        capitulo = DAOs.conseguirCapituloPorId(capituloId)
        if capitulo is None:
            return Response({'error': 'El capítulo no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarCapituloNombre(capitulo, nombre)
            return Response({'message': 'Nombre del capítulo actualizado con éxito'}, status=status.HTTP_200_OK)
    
class ActualizarCapituloDescripcionAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['capituloId', 'descripcion'],
            properties={
                'capituloId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del capítulo'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva descripción del capítulo')
            },
        ),
        responses={
            200: 'OK - Descripción del capítulo actualizada con éxito',
            400: 'Bad Request - El capítulo no existe'
        }
    )
    def post(self, request):
        capituloId = request.data.get('capituloId')
        descripcion = request.data.get('descripcion')
        capitulo = DAOs.conseguirCapituloPorId(capituloId)
        if capitulo is None:
            return Response({'error': 'El capítulo no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarCapituloDescripcion(capitulo, descripcion)
            return Response({'message': 'Descripción del capítulo actualizada con éxito'}, status=status.HTTP_200_OK)
        
class ActualizarCapituloPodcastAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['capituloId', 'miPodcast'],
            properties={
                'capituloId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del capítulo'),
                'miPodcast': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del podcast')
            },
        ),
        responses={
            200: 'OK - Podcast del capítulo actualizado con éxito',
            400: 'Bad Request - El capítulo no existe'
        }
    )
    def post(self, request):
        capituloId = request.data.get('capituloId')
        miPodcast = request.data.get('miPodcast')
        capitulo = DAOs.conseguirCapituloPorId(capituloId)
        miPodcast = DAOs.conseguirPodcastPorNombre(miPodcast)
        if capitulo is None:
            return Response({'error': 'El capítulo no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if miPodcast is None:
                return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                DAOs.actualizarCapituloPodcast(capitulo, miPodcast)
                return Response({'message': 'Podcast del capítulo actualizado con éxito'}, status=status.HTTP_200_OK)
            
class ActualizarCapituloArchivoAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['capituloId', 'nombreArchivoMp3'],
            properties={
                'capituloId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del capítulo'),
                'nombreArchivoMp3': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del archivo mp3')
            },
        ),
        responses={
            200: 'OK - Archivo del capítulo actualizado con éxito',
            400: 'Bad Request - El capítulo no existe'
        }
    )
    def post(self, request):
        capituloId = request.data.get('capituloId')
        nombreArchivoMp3 = request.data.get('nombreArchivoMp3')
        capitulo = DAOs.conseguirCapituloPorId(capituloId)
        if capitulo is None:
            return Response({'error': 'El capítulo no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            contenidoBinarioMp3 = convertirBinario(nombreArchivoMp3)
            DAOs.actualizarCapituloArchivoMp3(capitulo, contenidoBinarioMp3)
            return Response({'message': 'Archivo del capítulo actualizado con éxito'}, status=status.HTTP_200_OK)'''

'''EJEMPLO DE FORMATO JSON PARA LISTAR LOS CAPITULOS DE UN PODCAST
{
    "nombrePodcast": "podcast1"
}'''
class ListarCapitulosPodcastAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombrePodcast'],
            properties={
                'nombrePodcast': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del podcast')
            },
        ),
        responses={
            200: 'OK - Capitulos listados con éxito',
            400: 'Bad Request - El podcast no existe'}
    )
    def post(self, request):
        nombrePodcast = request.data.get('nombrePodcast')
        podcast = DAOs.conseguirPodcastPorNombre(nombrePodcast)
        if podcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            capitulos = DAOs.listarCapitulosPodcast(podcast)
            if capitulos:
                serializer = CapituloSerializer(capitulos, many=True)
                return Response({'capitulos': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay capitulos en el podcast'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR ARTISTA
{
    "nombre": "Kanye West",
    "nombreFoto": "Kanye_West.jpg",
    "descripcion": "Kanye West descrption here..."
}
'''
class CrearArtistaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre', 'nombreFoto', 'descripcion'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del artista'),
                'nombreFoto': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la foto del artista'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del artista')
            },
        ),
        responses={200: 'OK - Artista creado con éxito'}
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        foto = request.data.get('nombreFoto')
        descripcion = request.data.get('descripcion')
        contenidoBinarioFoto = convertirBinario(foto)
        artista = Artista(nombre=nombre, foto=contenidoBinarioFoto, descripcion=descripcion)
        DAOs.crearArtista(artista)
        return Response({'message': 'Artista creado con éxito'}, status=status.HTTP_200_OK)
    
'''EJEMPLO DE FORMATO JSON PARA CREAR PRESENTADOR
{
    "nombre": "Kanye West",
    "nombreFoto": "Kanye_West.jpg",
    "descripcion": "Kanye West descrption here..."
}
'''
class CrearPresentadorAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre', 'nombreFoto', 'descripcion'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del presentador'),
                'nombreFoto': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la foto del presentador'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del presentador')
            },
        ),
        responses={200: 'OK - Presentador creado con éxito'}
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        nombreFoto = request.data.get('nombreFoto')
        descripcion = request.data.get('descripcion')
        contenidoBinarioFoto = convertirBinario(nombreFoto)
        presentador = Presentador(nombre=nombre, foto=contenidoBinarioFoto, descripcion=descripcion)
        DAOs.crearPresentador(presentador)
        return Response({'message': 'Presentador creado con éxito'}, status=status.HTTP_200_OK)


'''EJEMPLO DE FORMATO JSON PARA LISTAR EL HISTORIAL DE UN USUARIO
{
    "correo": "sarah@gmail.com"
}'''
class ListarHistorialAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={
            200: 'OK - Historial listado con éxito',
            400: 'Bad Request - No tiene historial'
        }
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        historial = DAOs.listarHistorial(correo)
        if historial is not None:
            serializer = CancionSinAudioSerializer(historial, many=True)
            return Response({'historial': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene historial'}, status=status.HTTP_400_BAD_REQUEST)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN AL HISTORIAL DE UN USUARIO
{
    "correo": "sarah@gmail.com",
    "cancionId": "13"
}'''
class AgnadirCancionHistorialAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'cancionId'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'cancionId': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Canción añadida al historial con éxito',
            400: 'Bad Request - La canción no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        cancionId = request.data.get('cancionId') # coger el nombre de la cancion
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if cancion is None:
            return Response({'error': 'La canción no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if(DAOs.numeroCancionesHistorial(correo) >= 15): #Modificar buffer historial
                DAOs.eliminarUltimaCancionHistorial(correo)
                DAOs.agnadirCancionHistorial(correo, cancion)
                return Response({'message': 'Canción añadida al historial con éxito'}, status=status.HTTP_200_OK)
            else:
                DAOs.agnadirCancionHistorial(correo, cancion) #Todavia no hay 15 canciones
            return Response({'message': 'Canción añadida al historial con éxito'}, status=status.HTTP_200_OK)
    
# lo hacemos???
#class EliminarCancionHistorialAPI(APIView):
    
'''EJEMPLO DE FORMATO JSON PARA LISTAR LA COLA DE REPRODUCCIÓN DE UN USUARIO
{
    "correo": "sarah@gmail.com"
}'''
class ListarColaAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={
            200: 'OK - Cola listada con éxito',
            400: 'Bad Request - No tiene cola de reproducción'
        }
    )
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        queue = DAOs.listarCola(correo)
        if queue is not None:
            serializer = CancionSerializer(queue, many=True)
            return Response({'queue': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No tiene cola de reproducción'}, status=status.HTTP_400_BAD_REQUEST)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS CANCIONES DE UN ÁLBUM
{
    "nombreAlbum": "album de Sarah"
}'''
class ListarCancionesAlbumAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombreAlbum'],
            properties={
                'nombreAlbum': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del álbum')
            },
        ),
        responses={
            200: 'OK - Canciones listadas con éxito',
            400: 'Bad Request - No hay canciones en el álbum'
        }
    )
    def post(self, request):
        nombreAlbum = request.data.get('nombreAlbum')
        album = DAOs.conseguirAlbumPorNombre(nombreAlbum)
        if album is None:
            return Response({'error': 'El álbum no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            canciones = DAOs.listarCancionesAlbum(album)
            if canciones:
                serializer = CancionSerializer(canciones, many=True)
                return Response({'canciones': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay canciones en el álbum'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR GÉNERO
{
    "genero": "pop"
}'''
class CrearGeneroAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['genero', 'tipo'],
            properties={
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del género'),
                'tipo': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo del género (canción o podcast)')
            },
        ),
        responses={
            200: 'OK - Género creado con éxito',
            400: 'Bad Request - Tipo de género no válido'
        }
    )
    def post(self, request):
        nombre = request.data.get('genero')
        tipo = request.data.get('tipo')
        if tipo == 'Cancion' or tipo == 'Podcast':
            generoTipo = tipo
        else:
            return Response({'error': 'Tipo de género no válido'}, status=status.HTTP_400_BAD_REQUEST)
        genero = Genero(nombre=nombre, tipo=generoTipo)
        DAOs.crearGenero(genero)
        return Response({'message': 'Género creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR GÉNERO A UNA CANCIÓN
{
    "genero": "pop",
    "cancionId": "15"
}'''
class AgnadirGeneroCancionAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['genero', 'cancionId'],
            properties={
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del género'),
                'cancionId': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Género añadido con éxito',
            400: 'Bad Request - La canción o el género no existen'}
    )
    def post(self, request):
        generoNombre = request.data.get('genero')
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        genero = DAOs.conseguirGeneroPorNombre(generoNombre)
        if cancion is None or genero is None:
            return Response({'error': 'La canción o el género no existen'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.crearPertenecenCancion(genero, cancion)
            return Response({'message': 'Género añadido con éxito'}, status=status.HTTP_200_OK)
        
class AgnadirGeneroPodcastAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['genero', 'podcastId'],
            properties={
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del género'),
                'podcastId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast')
            },
        ),
        responses={
            200: 'OK - Género añadido con éxito',
            400: 'Bad Request - El podcast o el género no existen'}
    )
    def post(self, request):
        generoNombre = request.data.get('genero')
        podcastId = request.data.get('podcastId')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        genero = DAOs.conseguirGeneroPorNombre(generoNombre)
        if podcast is None or genero is None:
            return Response({'error': 'El podcast o el género no existen'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.crearPertenecenPodcast(genero, podcast)
            return Response({'message': 'Género añadido con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR CANTANTE A UNA CANCIÓN
{
    "artista": "2",
    "cancionId": "15"
}'''
class AgnadirCantanteAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['artistaId', 'cancionId'],
            properties={
                'artista': openapi.Schema(type=openapi.TYPE_STRING, description='ID del artista'),
                'cancionId': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Cantante añadido con éxito',
            400: 'Bad Request - El artista o la canción no existen'
        }
    )
    def post(self, request):
        artistaId = request.data.get('artistaId')
        cancionId = request.data.get('cancionId')
        artista = DAOs.conseguirArtistaPorId(artistaId)
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if artista is None or cancion is None:
            return Response({'error': 'El artista o la canción no existen'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.crearCantan(cancion, artista)
            return Response({'message': 'Cantante añadido con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR PRESENTADOR A UN PODCAST
{
    "presentador": "2",
    "podcastId": "15"
}'''
class AgnadirPresentadorAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['presentador', 'podcastId'],
            properties={
                'presentador': openapi.Schema(type=openapi.TYPE_STRING, description='ID del presentador'),
                'podcastId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast')
            },
        ),
        responses={200: 'OK - Presentador añadido con éxito'}
    )
    def post(self, request):
        presentadorId = request.data.get('presentador')
        podcastId = request.data.get('podcastId')
        presentador = DAOs.conseguirPresentadorPorId(presentadorId)
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if presentador is None or podcast is None:
            return Response({'error': 'El presentador o el podcast no existen'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.crearInterpretan(podcast, presentador)
            return Response({'message': 'Presentador añadido con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LOS ARTISTAS DE UNA CANCIÓN
{
    "cancionId": "33"
}'''
class ListarArtistasCancionAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cancionId'],
            properties={
                'cancionId': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Artistas listados con éxito',
            400: 'Bad Request - No hay artistas en la canción'
        }
    )
    def post(self, request):
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if cancion is None:
            return Response({'error': 'La canción no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            artistas = DAOs.listarArtistasCancion(cancion)
            if artistas:
                serializer = ArtistaSerializer(artistas, many=True)
                return Response({'artistas': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay artistas en la canción'}, status=status.HTTP_200_OK)
        

class ListarGenerosCancionAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cancionId'],
            properties={
                'cancionId': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Géneros listados con éxito',
            400: 'Bad Request - No hay géneros en la canción'
        }
    )
    def post(self, request):
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if cancion is None:
            return Response({'error': 'La canción no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            generos = DAOs.listarGenerosCancion(cancion)
            if generos:
                serializer = GeneroSerializer(generos, many=True)
                return Response({'generos': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'La canción no tiene géneros'}, status=status.HTTP_200_OK)

class ListarGenerosPodcastAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast')
            },
        ),
        responses={
            200: 'OK - Géneros listados con éxito',
            400: 'Bad Request - No hay géneros en el podcast'
        }
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if podcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            generos = DAOs.listarGenerosPodcast(podcast)
            if generos:
                serializer = GeneroSerializer(generos, many=True)
                return Response({'generos': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'El podcast no tiene géneros'}, status=status.HTTP_200_OK)
            
'''EJEMPLO DE FORMATO JSON PARA LISTAR LOS PRESENTADORES DE UN PODCAST
{
    "podcastId": "14"
}'''
class ListarPresentadoresPodcastAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast')
            },
        ),
        responses={
            200: 'OK - Presentadores listados con éxito',
            400: 'Bad Request - No hay presentadores en el podcast'
        }
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if podcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            presentadores = DAOs.listarPresentadoresPodcast(podcast)
            if presentadores:
                serializer = PresentadorSerializer(presentadores, many=True)
                return Response({'presentadores': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay presentadores en el podcast'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS CANCIONES DE UN GÉNERO
{
    "genero": "Pop"
}'''
class FiltrarCancionesPorGeneroAPI(APIView): # funciona #quizás aprovechar para los capitulos
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['genero'],
            properties={
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Género de las canciones a listar')
            },
        ),
        responses={200: 'OK - Canciones listadas con éxito'}
    )
    def post(self, request):
        generoNombre = request.data.get('genero')
        genero = DAOs.conseguirGeneroPorNombre(generoNombre)
        canciones = DAOs.listarCancionesGenero(genero)
        if canciones:
            serializer = CancionSerializer(canciones, many=True)
            return Response({'canciones': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay canciones en ese género'}, status=status.HTTP_200_OK)
        
class FiltrarPodcastsPorGeneroAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['genero'],
            properties={
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Género de los podcasts a listar')
            },
        ),
        responses={200: 'OK - Podcasts listados con éxito'}
    )
    def post(self, request):
        generoNombre = request.data.get('genero')
        genero = DAOs.conseguirGeneroPorNombre(generoNombre)
        podcasts = DAOs.listarPodcastsGenero(genero)
        if podcasts:
            serializer = PodcastSerializer(podcasts, many=True)
            return Response({'podcasts': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay podcasts en ese género'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR PODCAST
{
    "nombre": "podcast1",
    "nombreFoto": "foto.jpg",
    
}''' 
class CrearPodcastAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre', 'nombreFoto'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del podcast'),
                'nombreFoto': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la foto del podcast')
            },
        ),
        responses={200: 'OK - Podcast creado con éxito'}
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        nombreFoto = request.data.get('nombreFoto')
        #contenidoBinarioFoto = convertirBinario(nombreFoto)
        podcast = Podcast(nombre=nombre, puntuacion=0, numPuntuaciones=0, foto=nombreFoto)
        DAOs.crearPodcast(podcast)
        return Response({'message': 'Podcast creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR PODCAST
{
    "podcastId": "2",
    "nombre": "podcast2"
}'''
class ActualizarPodcastAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId', 'nombre'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del podcast'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre del podcast')
            },
        ),
        responses={
            200: 'OK - Podcast actualizado con éxito',
            400: 'Bad Request - El podcast no existe'
        }
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        nombre = request.data.get('nombre')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if podcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarPodcast(podcast, nombre)
            return Response({'message': 'Podcast actualizado con éxito'}, status=status.HTTP_200_OK)
    
'''class ActualizarPodcastNombreAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId', 'nombre'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del podcast'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre del podcast')
            },
        ),
        responses={
            200: 'OK - Nombre del podcast actualizado con éxito',
            400: 'Bad Request - El podcast no existe'
        }
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        nombre = request.data.get('nombre')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if podcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.actualizarPodcastNombre(podcast, nombre)
            return Response({'message': 'Nombre del podcast actualizado con éxito'}, status=status.HTTP_200_OK)
        
class ActualizarPodcastFotoAPI(APIView): # funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId', 'nombreFoto'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del podcast'),
                'nombreFoto': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la foto del podcast')
            },
        ),
        responses={
            200: 'OK - Foto del podcast actualizada con éxito',
            400: 'Bad Request - El podcast no existe'
        }
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        nombreFoto = request.data.get('nombreFoto')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if podcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            contenidoBinarioFoto = convertirBinario(nombreFoto)
            DAOs.actualizarPodcastFoto(podcast, contenidoBinarioFoto)
            return Response({'message': 'Foto del podcast actualizada con éxito'}, status=status.HTTP_200_OK)'''

'''
EJEMPLO DE BUSCAR ARTISTA
{
    "artist_name": "Kanye West"
}



class BuscarArtistaSPOTY(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Obtain token using the get_token() function
        token = get_token()

        # Check if token is obtained
        if token:
            artist_name = request.data.get('artist_name')
            url = "https://api.spotify.com/v1/search?q="
            headers = get_auth_header(token)
            query = f"{artist_name}&type=artist&limit=1"
            query_url = url + query
            artist_response = get(query_url, headers=headers)

            # Check if response is successful
            if artist_response.status_code == 200:
                json_artist = artist_response.json()
                return Response({'artist': json_artist}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed to retrieve artist information'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Failed to obtain access token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)'''

'''
EJEMPLO DE BUSCAR
{
    "nombre": "a"
}'''
class BuscarAPI(APIView): #funciona, hay que conseguir que busque entre todo lo de debajo
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del objeto a buscar')
            },
        ),
        responses={
            200: 'OK - Se encontraron resultados',
            404: 'Not Found - No se encontraron resultados'
        },
        operation_description='Buscar objetos por nombre',
    )
    def post(self, request):
        nombre_objeto = request.data.get('nombre')
        resultados = []
        objeto = DAOs.buscarCancion(nombre_objeto)
        if objeto is not None:
            serializer = CancionSerializer(objeto, many=True)
            resultados.extend([{'cancion': data} for data in serializer.data])
        objeto = DAOs.buscarCapitulo(nombre_objeto)
        if objeto is not None:
            serializer = CapituloSerializer(objeto, many=True)
            resultados.extend([{'capitulo': data} for data in serializer.data])
        objeto = DAOs.buscarPodcast(nombre_objeto)
        if objeto is not None:
            serializer = PodcastSerializer(objeto, many=True)
            resultados.extend([{'podcast': data} for data in serializer.data])
        objeto = DAOs.buscarArtista(nombre_objeto)
        if objeto is not None:
            serializer = ArtistaSerializer(objeto, many=True)
            resultados.extend([{'artista': data} for data in serializer.data])
        objeto = DAOs.buscarAlbum(nombre_objeto)
        if objeto is not None:
            serializer = AlbumSerializer(objeto, many=True)
            resultados.extend([{'album': data} for data in serializer.data])
        objeto = DAOs.buscarPlaylist(nombre_objeto)
        if objeto is not None:
            serializer = PlaylistSerializer(objeto, many=True)
            resultados.extend([{'playlist': data} for data in serializer.data])
        objeto = DAOs.buscarPresentador(nombre_objeto)
        if objeto is not None:
            serializer = PresentadorSerializer(objeto, many=True)
            resultados.extend([{'presentador': data} for data in serializer.data])
        objeto = DAOs.buscarUsuario(nombre_objeto)
        if objeto is not None:
            serializer = UsuarioSerializer(objeto, many=True)
            resultados.extend([{'usuario': data} for data in serializer.data])
        if resultados:
            return Response(resultados, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No se han encontrado coincidencias'}, status=status.HTTP_404_NOT_FOUND)


class RecomendarAPI(APIView): #comprobar
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario')
            },
        ),
        responses={
            200: 'OK - Recomendaciones listadas con éxito',
            400: 'Bad Request - El usuario no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        usuario = DAOs.conseguirUsuarioPorCorreo(correo)
        if usuario is None:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            artistaFavorito = DAOs.devolverArtistaFavorito(correo)
            presentadorFavorito = DAOs.devolverPresentadorFavorito(correo)
            generoFavoritoCancion = DAOs.devolverGeneroFavoritoCancion(correo)
            generoFavoritoPodcast = DAOs.devolverGeneroFavoritoPodcast(correo)
            canciones = DAOs.listarCanciones()
            podcasts = DAOs.listarPodcasts()
            if artistaFavorito is None or presentadorFavorito is None or generoFavoritoCancion is None or generoFavoritoPodcast is None:
                
                cancion1 = random.sample(list(canciones), 1)
                canciones = [cancion for cancion in canciones if cancion not in cancion1]
                cancion2 = random.sample(canciones, 1)
                podcast1 = random.sample(list(podcasts), 1)
                podcasts = [podcast for podcast in podcasts if podcast not in podcast1]
                podcast2 = random.sample(podcasts, 1)
                resultadosCanciones = cancion1 + cancion2
                resultadosPodcasts = podcast1 + podcast2
            else:
                cancionArtista = random.sample(DAOs.listarCancionesArtista(artistaFavorito), 1)
                canciones = [cancion for cancion in canciones if cancion not in cancionArtista]
                cancionGeneroCancion = random.sample(DAOs.listarCancionesGenero(generoFavoritoCancion), 1)
                while cancionGeneroCancion in cancionArtista:
                    cancionGeneroCancion = random.sample(DAOs.listarCancionesGenero(generoFavoritoCancion), 1)
                podcastPresentador = random.sample(DAOs.listarPodcastsPresentador(presentadorFavorito), 1)
                podcasts = [podcast for podcast in podcasts if podcast not in podcastPresentador]
                podcastGeneroPodcast = random.sample(DAOs.listarPodcastsGenero(generoFavoritoPodcast), 1)
                while podcastGeneroPodcast in podcastPresentador:
                    podcastGeneroPodcast = random.sample(DAOs.listarPodcastsGenero(generoFavoritoPodcast), 1)
                resultadosCanciones = cancionArtista + cancionGeneroCancion
                resultadosPodcasts = podcastPresentador + podcastGeneroPodcast
            serializerCanciones = CancionSerializer(resultadosCanciones, many=True)
            serializerPodcasts = PodcastSerializer(resultadosPodcasts, many=True)
            return Response({'recomendaciones': {'canciones': serializerCanciones.data, 'podcasts': serializerPodcasts.data}}, status=status.HTTP_200_OK)
               
class AgnadirGeneroFavoritoAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'genero'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'genero': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del género')
            },
        ),
        responses={
            200: 'OK - Género favorito añadido con éxito',
            400: 'Bad Request - El género no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        nombreGenero = request.data.get('genero')
        genero = DAOs.conseguirGeneroPorNombre(nombreGenero)
        if genero is None:
            return Response({'error': 'El género no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.agnadirGeneroFavorito(correo, genero)
            return Response({'message': 'Género favorito añadido con éxito'}, status=status.HTTP_200_OK)
        
class AgnadirArtistaFavoritoAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'artista'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'artistaId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del artista')
            },
        ),
        responses={
            200: 'OK - Artista favorito añadido con éxito',
            400: 'Bad Request - El artista no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        artistaId = request.data.get('artistaId')
        artista = DAOs.conseguirArtistaPorId(artistaId)
        if artista is None:
            return Response({'error': 'El artista no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.agnadirArtistaFavorito(correo, artista)
            return Response({'message': 'Artista favorito añadido con éxito'}, status=status.HTTP_200_OK)

class AgnadirPresentadorFavoritoAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['correo', 'presentador'],
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'presentadorId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del presentador')
            },
        ),
        responses={
            200: 'OK - Presentador favorito añadido con éxito',
            400: 'Bad Request - El presentador no existe'
        }
    )
    def post(self, request):
        correo = request.data.get('correo')
        presentadorId = request.data.get('presentadorId')
        presentador = DAOs.conseguirPresentadorPorId(presentadorId)
        if presentador is None:
            return Response({'error': 'El presentador no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.agnadirPresentadorFavorito(correo, presentador)
            return Response({'message': 'Presentador favorito añadido con éxito'}, status=status.HTTP_200_OK)
        
class GenerosCancionesAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Géneros listados con éxito'}
    )
    def get(self, request):
        generos = DAOs.listarGenerosCanciones()
        serializer = GeneroSerializer(generos, many=True)
        return Response({'generos': serializer.data}, status=status.HTTP_200_OK)
    
class GenerosPodcastsAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Géneros listados con éxito'}
    )
    def get(self, request):
        generos = DAOs.listarGenerosPodcasts()
        serializer = GeneroSerializer(generos, many=True)
        return Response({'generos': serializer.data}, status=status.HTTP_200_OK)
    
class PresentadoresAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Presentadores listados con éxito'}
    )
    def get(self, request):
        presentadores = DAOs.listarPresentadores()
        serializer = PresentadorSerializer(presentadores, many=True)
        return Response({'presentadores': serializer.data}, status=status.HTTP_200_OK)
    
class ArtistasAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        responses={200: 'OK - Artistas listados con éxito'}
    )
    def get(self, request):
        artistas = DAOs.listarArtistas()
        serializer = ArtistaSerializer(artistas, many=True)
        return Response({'artistas': serializer.data}, status=status.HTTP_200_OK)

class EditarTipoGeneroAPI(APIView): #funciona
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nombre', 'esDeCancion'],
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del género'),
                'esDeCancion': openapi.Schema(type=openapi.TYPE_INTEGER, description='El género es de canción (1) o de podcast (0)')
            },
        ),
        responses={
            200: 'OK - Tipo de género editado con éxito',
            400: 'Bad Request - El género no existe'
        }
    )
    def post(self, request):
        nombre = request.data.get('nombre')
        esDeCancion = request.data.get('esDeCancion')
        genero = DAOs.conseguirGeneroPorNombre(nombre)
        if genero is None:
            return Response({'error': 'El género no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if esDeCancion == 1:
                DAOs.editarTipoGenero(genero, "Cancion")
            else:
                DAOs.editarTipoGenero(genero, "Podcast")
                return Response({'message': 'Tipo de género editado con éxito'}, status=status.HTTP_200_OK)
           
class EliminarCancionAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cancionId'],
            properties={
                'cancionId': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la canción')
            },
        ),
        responses={
            200: 'OK - Canción eliminada con éxito',
            400: 'Bad Request - La canción no existe'
        }
    )
    def post(self, request):
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        if cancion is None:
            return Response({'error': 'La canción no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.eliminarCancion(cancion)
            return Response({'message': 'Canción eliminada con éxito'}, status=status.HTTP_200_OK)
        
class EliminarPodcastAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['podcastId'],
            properties={
                'podcastId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast')
            },
        ),
        responses={
            200: 'OK - Podcast eliminado con éxito',
            400: 'Bad Request - El podcast no existe'
        }
    )
    def post(self, request):
        podcastId = request.data.get('podcastId')
        podcast = DAOs.conseguirPodcastPorId(podcastId)
        if podcast is None:
            return Response({'error': 'El podcast no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.eliminarPodcast(podcast)
            return Response({'message': 'Podcast eliminado con éxito'}, status=status.HTTP_200_OK)
        
class EliminarCapituloAPI(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['capituloId'],
            properties={
                'capituloId': openapi.Schema(type=openapi.TYPE_STRING, description='ID del capítulo')
            },
        ),
        responses={
            200: 'OK - Capítulo eliminado con éxito',
            400: 'Bad Request - El capítulo no existe'
        }
    )
    def post(self, request):
        capituloId = request.data.get('capituloId')
        capitulo = DAOs.conseguirCapituloPorId(capituloId)
        if capitulo is None:
            return Response({'error': 'El capítulo no existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.eliminarCapitulo(capitulo)
            return Response({'message': 'Capítulo eliminado con éxito'}, status=status.HTTP_200_OK)