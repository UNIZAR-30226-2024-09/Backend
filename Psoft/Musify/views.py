from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Usuario, Amigo, Cancion, Podcast, Capitulo, Playlist, Colabora, Contiene, Historial, Cola, Genero, Pertenecen, Album, Artista, CustomToken
from . import DAOs
from Psoft.serializers import UsuarioSerializer, CancionSerializer, AmigosSerializer, PlaylistSerializer, HistorialSerializer, ColaSerializer, CapituloSerializer, PodcastSerializer, AlbumSerializer, ArtistaSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token

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

# CORREO DE VERIFICACIÓN
#def send_verification_email(user, request):
#   current_site = get_current_site(request)
#   subject = 'Verifica tu cuenta de Musify'
#   message = render_to_string('authentication/activate.html', {
#       'user': user,
#       'domain': current_site,
#       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#       'token': generate_token.make_token(user)
#})

#def activate_user(request, uidb64, token):
#    try:
#       uid = force_text(urlsafe_base64_decode(uidb64))
#       user = Usuario.objects.get(pk=uid)
#    except Exception as e:
#       user = None
#    if user and generate_token.check_token(user, token):
#       user.is_email_verified = True
#       user.save()
#       messages.add_message(request, messages.SUCCESS, 'Cuenta verificada con éxito')
#       return redirect(reverse('login'))
''''

def home(request):
    text = "Home page"
    return HttpResponse(text, content_type='text/plain')

def test_are_friends(request):
    # Crear usuario
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    #DAOs.create_user(user_vo)
    # Crear amigo
    amigo_vo = DAOs.get_user_by_correo("PacoAmigo@gmail.com")
    #DAOs.create_user(amigo_vo)
    #DAOs.add_friend(user_vo.correo, amigo_vo.correo)
    if DAOs.are_friends(user_vo.correo,amigo_vo.correo) == True:
        friends = DAOs.get_friends(user_vo.correo)
        print("Amigos de Paco: ")
        for friend in friends:
            
            print(friend.correo + "\n")
    return HttpResponse(status=200)

def test_crear_playlist(request):
    # Crear usuario
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com") #Esto en caso real se coge de la sesion
    # Crear playlist
    #DAOs.create_playlist(user_vo.correo, "Playlist de Paco", True)
    Playlists = DAOs.get_playlists_from_user(user_vo.correo)
    DAOs.update_playlist_details(Playlists[0].id, "Playlist Privada de Paco", False)
    #DAOs.create_song("Cancion de Paco")
    cancion = DAOs.get_song_by_id(2)
    #DAOs.add_song_to_playlist(Playlists[0].id,cancion.id)
    Canciones = DAOs.get_songs_from_playlist(1)
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
    return HttpResponse(status=200)

def test_queue_view(request):
    
    user = DAOs.get_user_by_correo("Paco@gmail.com")
    
    #DAOs.add_song_to_queue(user.correo, 2)
    queue = DAOs.get_queue_from_user(user.correo)
    # You can render these queue items in your template or just print them for testing
    for item in queue:
        print("Song:", item.nombre)
        print("Artist(s):", item.cantantes if item.cantantes else "N/A")
        print("Album:", item.miAlbum.nombre if item.miAlbum else "N/A")
        print()
    
    return HttpResponse(status=200)    

def test_password_view(request):
    user_vo = DAOs.get_user_by_correo("nerea@ejemplo.com")
    DAOs.check_user_password(user_vo, "nerea")
    if DAOs.check_user_password(user_vo, "nerea") == True:
        print("Contraseña correcta")
    else:
        print("Contraseña incorrecta")
    return HttpResponse(status=200)

# COMPROBADO pero quitando campos de Cancion de models.py
def test_add_song_to_history(request):
    cantantes='a, b, c'
    album_vo = DAOs.get_album_by_id(1)
    song_vo = Cancion(
        nombre='cancion3',
        #letra=' ',
        #cantantes.set('a', 'b'), no se qué hay que poner aquí
        miAlbum=album_vo,
        puntuacion='5'
    )
    DAOs.create_song(song_vo)

    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    song_vo = DAOs.get_song_by_id(16)
    DAOs.add_song_to_history(user_vo.correo, song_vo.id)
    history = DAOs.get_user_history("Paco@gmail.com")
    if history != None:
        for song in history:
            print(song.nombre + "\n")
    else :
        print("No hay canciones en el historial")
    return HttpResponse(status=200)

# COMPROBADO
def test_remove_user(request):
    nuevo_usuario = Usuario(
        correo='ejemplo@gmail.com',
        nombre='ej',
        sexo='',
        nacimiento='2000-5-25',
        contrasegna='ej',
        pais=''
    )
    DAOs.create_user(nuevo_usuario)
    DAOs.remove_user('ejemplo@gmail.com')
    existe = DAOs.exists_user('ejemplo@gmail.com')
    if existe == False:
        print("Usuario eliminado")
    else:
        print("Usuario no eliminado")
    return HttpResponse(status=200)

#COMPROBADO
def test_add_friend(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    nuevo_amigo = Usuario(
        correo='PacoAmigo3@gmail.com',
        nombre='PacoAmigo3',
        sexo='',
        nacimiento='2001-9-5',
        contrasegna='PacoAmigo3',
        pais=''
    )
    nuevo_amigo=DAOs.create_user(nuevo_amigo)
    nuevo_amigo = DAOs.get_user_by_correo("pacoamigo3@gmail.com")
    DAOs.add_friend(user_vo.correo, nuevo_amigo.correo)
    friends = DAOs.get_friends(user_vo.correo)
    print("Amigos de Paco: ")
    for friend in friends:
        print(friend.correo + "\n")
    return HttpResponse(status=200)

# COMPROBADO pero no se pq no saca cosas por la terminal
def test_song(request):
    album_vo = DAOs.get_album_by_id(11)
    nueva_cancion = Cancion(
        #letra='letra',
        #cantantes='cantantes',
        miAlbum=album_vo,
        puntuacion=3.5,
        nombre="cancion6"
    )
    DAOs.create_song(nueva_cancion)
    DAOs.add_song_to_playlist(1, DAOs.get_song_by_name("cancion6").id)
    Canciones = DAOs.get_songs_from_playlist(5)
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
            DAOs.add_song_rating(DAOs.get_song_by_name("cancion6").id, 5)
            print(DAOs.get_song_rating(DAOs.get_song_by_name("cancion6").id))
            print(DAOs.get_song_album(DAOs.get_song_by_name("cancion6").id))
            print(DAOs.get_song_artists(DAOs.get_song_by_name("cancion6").id))
    return HttpResponse(status=200)     

# COMPROBADO
def test_update_user(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    print("datos anteriores de " + "\n" + user_vo.correo + "\n"  + user_vo.nombre + "\n" + user_vo.sexo + "\n" + str(user_vo.nacimiento) + "\n" + user_vo.contrasegna + "\n" + user_vo.pais + "\n")
    usuario_actualizado = Usuario(
        correo = "Paco@gmail.com",
        nombre='paco',
        sexo='M',
        nacimiento=timezone.now(),
        contrasegna='Paquito',
        pais='Espana'
    )
    DAOs.update_user(usuario_actualizado)
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    print("datos actuales de " + "\n" + user_vo.correo + "\n"  + user_vo.nombre + "\n" + user_vo.sexo + "\n" + str(user_vo.nacimiento) + "\n" + user_vo.contrasegna + "\n" + user_vo.pais + "\n")
    return HttpResponse(status=200)

# COMPROBADO
def test_remove_friend(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    nuevo_amigo = DAOs.get_user_by_correo("pacoamigo2@gmail.com")
    DAOs.remove_friend(user_vo.correo, nuevo_amigo.correo)
    return HttpResponse(status=200)

# COMPROBADO
def test_get_genre_songs(request):
        #genre_vo = DAOs.create_genre('pop')
    genre_vo = DAOs.get_genre_by_name('pop')
    song_vo=DAOs.get_song_by_id(6)
    pertenecen_vo = Pertenecen(
        miGenero=genre_vo,
        miAudio=song_vo
    )
    DAOs.create_pertenecen(genre_vo, song_vo)
    songs=DAOs.get_genre_songs(genre_vo.nombre)
    #for song in songs:
    #    print(song.nombre + "\n")
    return HttpResponse(status=200)


# COMPROBADO
def test_remove_song_from_history(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    song_vo = DAOs.get_song_by_name("cancion1")
    historial_vo = DAOs.get_user_history(user_vo.correo)
    print("Historial de Paco antes de eliminar cancion1: ")
    if historial_vo != None:
        for song in historial_vo:
            print(song.nombre + "\n")
    DAOs.remove_song_from_history(user_vo.correo, song_vo.id)
    print("Historial de Paco despues de eliminar cancion1: ")
    historial_vo = DAOs.get_user_history(user_vo.correo)
    if historial_vo != None:
        for song in historial_vo:
            print(song.nombre + "\n")
    return HttpResponse(status=200)


#COMPROBADO
def test_remove_song_from_queue(request):
    user_vo = DAOs.get_user_by_correo("john.doe@example.com")
    song_vo = DAOs.get_song_by_id(15)
    DAOs.add_song_to_queue(user_vo.correo, song_vo.id)
    print("Cola después de añadir una cancion: ")
    songs = DAOs.get_queue_from_user(user_vo.correo)
    for song in songs:
        print(song.nombre + "\n")
    DAOs.remove_song_from_queue(user_vo.correo, song_vo.id)
    print("Cola después de eliminar la cancion: ")
    songs = DAOs.get_queue_from_user(user_vo.correo)
    for song in songs:
        print(song.nombre + "\n")
    return HttpResponse(status=200)

#COMPROBADO
def test_remove_song_from_playlist(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    Playlists = DAOs.get_playlists_from_user(user_vo.correo)
    cancion = DAOs.get_song_by_id(21)
    Canciones = DAOs.get_songs_from_playlist(1)
    print("Canciones de la playlist antes de eliminar una cancion: ")
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
    DAOs.remove_song_from_playlist(Playlists[0].id,cancion.id)
    print("Canciones de la playlist despues de eliminar una cancion: ")
    Canciones = DAOs.get_songs_from_playlist(1)
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
    return HttpResponse(status=200)

# COMPROBADO
def test_album(request):
    album_vo = Album(
        nombre='album de Paco5'
    )
    album_vo = DAOs.create_album(album_vo)
    print(DAOs.get_album_by_name("album de Paco5").nombre)
    canciones = DAOs.get_album_songs(album_vo)
    print("Canciones del album de Paco5 antes de añadir cancion2: ")
    for cancion in canciones:
        print(cancion.nombre + "\n")
    print("Canciones del album de Paco5 despues de añadir cancion2: ")
    cancion_vo = DAOs.get_song_by_name("cancion2")
    DAOs.add_song_to_album(album_vo, cancion_vo)
    canciones = DAOs.get_album_songs(album_vo)
    for cancion in canciones:
        print(cancion.nombre + "\n")
    return HttpResponse(status=200)

'''

#API
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
    def post(self, request):
        
        correo = request.data.get('correo')
        contrasegna = request.data.get('contrasegna')

        # Autenticar al usuario
        usuario = authenticate(correo=correo, contrasegna=contrasegna)

        if usuario is not None:
            # El usuario ha sido autenticado, devolver respuesta de éxito
            token, created = CustomToken.objects.get_or_create(usuario=usuario)
            return Response({'message': 'Inicio de sesión correcto',"token": token.key}, status=status.HTTP_200_OK)
        else:
            # El usuario no ha sido autenticado, devolver respuesta de error
            return Response({'error': 'Correo o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)

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
class RegistroAPI(APIView): # funciona
    permission_classes = [AllowAny]

    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        sexo = request.data.get('sexo')
        nacimiento = request.data.get('nacimiento')
        contrasegna = request.data.get('contrasegna')
        pais = request.data.get('pais')
        generos_seleccionados = request.POST.getlist('generos') # no se si es post o data
        artistas_seleccionados = request.POST.getlist('artistas') # no se si es post o data

        if not nombre:
            return Response({'error': 'Nombre es un campo obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f'Nombre recibido: {nombre}')

        usuario = Usuario(correo=correo, nombre=nombre, sexo=sexo, nacimiento=nacimiento, contrasegna=contrasegna, pais=pais)

        if Usuario.objects.filter(correo=correo).exists():
            return Response({'error': 'El correo introducido ya tiene asociada una cuenta'}, status=status.HTTP_400_BAD_REQUEST)

        DAOs.crearUsuario(usuario)
        DAOs.crearPlaylist(correo,"Favoritos",False)
        token = CustomToken.objects.create(usuario=usuario)
        return Response({'message': 'Usuario registrado con éxito',"token": token.key}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR USUARIO
{
    "correo": "john.doe@example.com",
    "nombre": "John Doe",
    "sexo": "Male",
    "nacimiento": "1985-03-10",
    "contrasegna": "5U3rP@55w0rd",
    "pais": "United States"
}
'''

class ActualizarUsuarioAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        sexo = request.data.get('sexo')
        nacimiento = request.data.get('nacimiento')
        contrasegna = request.data.get('contrasegna')
        pais = request.data.get('pais')
        usuario = Usuario(correo=correo, nombre=nombre, sexo=sexo, nacimiento=nacimiento, contrasegna=contrasegna, pais=pais)
        DAOs.actualizarUsuario(usuario)
        return Response({'message': 'Usuario actualizado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ELIMINAR USUARIO
{
    "correo": "john.doe@example.com"
}
'''
class EliminarUsuarioAPI(APIView): #funciona
    permission_classes = [AllowAny]
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
class SeguirAmigoAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        amigo = request.data.get('amigo') # coger el correo del amigo
        DAOs.agnadirAmigo(correo, amigo)
        return Response({'message': 'Amigo añadido con éxito'}, status=status.HTTP_200_OK) 
    
'''EJEMPLO DE FORMATO JSON PARA LISTAR AMIGOS
{
    "correo": "Paco@gmail.com"
}'''
class ListarAmigosAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        amigos = DAOs.listarAmigos(correo)
        if amigos:
            serializer = AmigosSerializer(amigos, many=True)
            return Response({'amigos': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene amigos'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA DEJAR DE SEGUIR A UN AMIGO
{
    "correo": "john.doe@example.com",
    "amigo": "sarah@gmail.com"
}
'''
class DejarDeSeguirAmigoAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        amigo = request.data.get('amigo')
        DAOs.eliminarAmigo(correo, amigo)
        return Response({'message': 'Amigo eliminado con éxito'}, status=status.HTTP_200_OK)
    
'''EJEMPLO DE FORMATO JSON PARA COMPROBAR SI DOS USUARIOS SON AMIGOS
{
    "correo": "john.doe@example.com",
    "amigo": "sarah@gmail.com"
}
'''
class SonAmigosAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        amigo = request.data.get('amigo')
        if DAOs.sonAmigos(correo, amigo) == True:
            return Response({'message': 'Son amigos'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No son amigos'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR UNA PLAYLIST        
{
    "correo": "sarah@gmail.com",
    "nombre": "Playlist de Paco",
    "publica": true
}'''
class CrearPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
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

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR UNA PLAYLIST
{
    "playlistId": "2",
    "nombre": "Playlist de Sarah",
    "publica": "False"
}'''

class ActualizarPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        playlistId = request.data.get('playlistId')
        nombre = request.data.get('nombre')
        publica = request.data.get('publica')
        DAOs.actualizarPlaylist(playlistId, nombre, publica)
        return Response({'message': 'La playlist ha sido actualizada con éxito'}, status=status.HTTP_200_OK)
    
class ListarCancionesAPI(APIView): # funciona
    permission_classes = [AllowAny]

    def post(self, request):
        canciones = DAOs.listarCanciones()
        canciones[:3] #QUITAR EN VERSION FUNCIONAL, HECHO PARA TESTEAR HOY YA QUE NO ESTA DEL TODO TERMINADO
        # Verificar si se encontraron canciones en la playlist
        if canciones:
            serializer = CancionSerializer(canciones, many=True)
            # Devolver la lista de canciones serializadas en formato JSON
            return Response({'canciones': serializer.data}, status=status.HTTP_200_OK)
        else:
            # Si no se encontraron canciones, devolver un mensaje indicando lo mismo
            return Response({'message': 'No hay canciones'}, status=status.HTTP_200_OK)
        
class ListarPodcastsAPI(APIView): # funciona
    permission_classes = [AllowAny]

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
        
'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN A UNA PLAYLIST
{
    "playlistId": "2",
    "cancionId": "26"
}'''

class AgnadirCancionPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
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
    "puntuacion": "5",
    "nombreArchivoMp3": "Kanye West - Homecoming_LQ488QrqGE4.mp3"
}'''

def convertirBinario(ruta):
    #entre las comillas y antes de las dos barras hay que poner la ruta del archivo, teniendo en cuenta que ruta tiene el nombre del archivo
    with open(r"C:\Users\nerea\OneDrive\Escritorio\Inginformatica\3o\Proyecto_software\Prácticas\\" + ruta, "rb") as archivo:
        contenido_binario = archivo.read()
        contenido_base64 = base64.b64encode(contenido_binario)
    return contenido_base64

class CrearCancionAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        nombreFoto = request.data.get('nombreFoto')
        miAlbum = request.data.get('miAlbum')
        puntuacion = 0 # cuando se crea la canción en nuestra app, se crea con puntuación 0
        numeroPuntuaciones = 0
        nombreMp3 = request.data.get('nombreArchivoMp3')
        if miAlbum != '':
            miAlbum = DAOs.conseguirAlbumPorId(miAlbum)
        else:
            miAlbum = None
        contenidoBinarioMp3 = convertirBinario(nombreMp3)
        contenidoBinarioFoto = convertirBinario(nombreFoto)
        cancion = Cancion(nombre=nombre, miAlbum=miAlbum, puntuacion=puntuacion, numPuntuaciones=numeroPuntuaciones, archivoMp3=contenidoBinarioMp3, foto=contenidoBinarioFoto)
        DAOs.crearCancion(cancion)
        return Response({'message': 'Canción creada con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA PUNTUAR UNA CANCIÓN
{}
    "cancionId": "27",
    "puntuacion": "4"
}'''

class PuntuarCancionAPI(APIView): # comprobar
    permission_classes = [AllowAny]
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
    def post(self, request):
        correo = request.data.get('correo')
        cancionId = request.data.get('cancionId')
        cancionVO = DAOs.conseguirCancionPorId(cancionId)
        if cancionVO is not None:
            if DAOs.cancionFavorita(correo, cancionVO):
                return Response({'message': 'La canción está en favoritos'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'La canción no está en favoritos'}, status=status.HTTP_200_OK)
        

'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN A LA COLA DE REPRODUCCIÓN
{
    "correo": "sarah@gmail.com",
    "cancionId": "27"
}'''

class AgnadirCancionColaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        cancionId = request.data.get('cancionId')
        DAOs.agnadirCancionCola(correo, cancionId)
        return Response({'message': 'Canción añadida a la cola de reproducción con éxito'}, status=status.HTTP_200_OK)

class EliminarCancionColaAPI(APIView): # funciona
    permission_classes = [AllowAny]
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
    def post(self, request):
        nombre = request.data.get('nombre')
        album = Album(nombre=nombre)
        DAOs.crearAlbum(album)
        return Response({'message': 'Álbum creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR ÁLBUM
{
    "albumId": "1",
    "nombre": "album de Sarah"
}'''
class ActualizarAlbumAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        albumId = request.data.get('albumId')
        nombre = request.data.get('nombre')
        album = Album(id=albumId, nombre=nombre)
        DAOs.actualizarAlbum(album)
        return Response({'message': 'Álbum actualizado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR AÑADIR CANCIÓN A UN ÁLBUM
{
    "albumNombre": "album de Sarah",
    "cancionNombre": "Buenas tardes"
}'''

class AgnadirCancionAlbumAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        albumNombre = request.data.get('albumNombre')
        album = DAOs.conseguirAlbumPorNombre(albumNombre)
        cancionNombre = request.data.get('cancionNombre')
        cancion = DAOs.conseguirCancionPorNombre(cancionNombre)
        if Cancion.objects.filter(nombre=cancionNombre, miAlbum=album).exists():
            return Response({'message': 'La cancion ya existe está en el álbum'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.agnadirCancionAlbum(album, cancion)
        return Response({'message': 'Canción añadida al álbum con éxito'}, status=status.HTTP_200_OK)

class PuntuarPodcastAPI(APIView): #comprobar
    permission_classes = [AllowAny]
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
    def post(self, request):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        podcastId = request.data.get('podcastId')
        nombreArchivoMp3 = request.data.get('nombreArchivoMp3')

        if not nombre:
            return Response({'error': 'Nombre es un campo obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
        if podcastId != '':
            miPodcast = DAOs.conseguirPodcastPorId(podcastId)
        else:
            miPodcast = None
        contenidoBinarioMp3 = convertirBinario(nombreArchivoMp3)
        capitulo = Capitulo(nombre=nombre, descripcion=descripcion, miPodcast=miPodcast, archivoMp3=contenidoBinarioMp3)
        DAOs.crearCapitulo(capitulo)
        return Response({'message': 'Capítulo almacenado correctamente'}, status=status.HTTP_200_OK)



'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR CAPITULO
{
    "capituloId": "1",
    "nombre": "episodio1",
    "descripcion": "descripcion del epidodio1",
    "miPodcast": "podcast2" 
}'''
class ActualizarCapituloAPI(APIView): #funciona
    permission_classes = [AllowAny]
    def post(self, request):
        capituloId = request.data.get('capituloId')
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        miPodcast = request.data.get('miPodcast')
        miPodcast = DAOs.conseguirPodcastPorNombre(miPodcast)
        'capitulo = Capitulo(nombre=nombre, descripcion=descripcion, miPodcast=miPodcast)'
        DAOs.actualizarCapitulo(capituloId, nombre, descripcion, miPodcast)
        return Response({'message': 'Capítulo actualizado con éxito'}, status=status.HTTP_200_OK)
    
'''EJEMPLO DE FORMATO JSON PARA LISTAR LOS CAPITULOS DE UN PODCAST
{
    "nombrePodcast": "podcast1"
}'''
class ListarCapitulosPodcastAPI(APIView): #funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombrePodcast = request.data.get('nombrePodcast')
        podcast = DAOs.conseguirPodcastPorNombre(nombrePodcast)
        capitulos = DAOs.listarCapitulosPodcast(podcast)
        if capitulos:
            serializer = CapituloSerializer(capitulos, many=True)
            return Response({'capitulos': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay capitulos en el podcast'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR ARTISTA
{
    "nombre": "Kanye West",
    "descripcion": "Kanye West descrption here..."
}
'''
class CrearArtistaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        artista = Artista(nombre=nombre, descripcion=descripcion)
        DAOs.crearArtista(artista)
        return Response({'message': 'Artista creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR EL HISTORIAL DE UN USUARIO
{
    "correo": "sarah@gmail.com"
}'''
class ListarHistorialAPI(APIView): #funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        historial = DAOs.listarHistorial(correo)
        if historial:
            serializer = CancionSerializer(historial, many=True)
            return Response({'historial': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene historial'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN AL HISTORIAL DE UN USUARIO
{
    "correo": "sarah@gmail.com",
    "cancion_nombre": "Buenas tardes"
}'''

class AgnadirCancionHistorialAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        cancion_nombre = request.data.get('cancion_nombre') # coger el nombre de la cancion
        cancion = DAOs.conseguirCancionPorNombre(cancion_nombre)
        DAOs.agnadirCancionHistorial(correo, cancion)
        return Response({'message': 'Canción añadida al historial con éxito'}, status=status.HTTP_200_OK)
    
# lo hacemos???
#class EliminarCancionHistorialAPI(APIView):
    
'''EJEMPLO DE FORMATO JSON PARA LISTAR LA COLA DE REPRODUCCIÓN DE UN USUARIO
{
    "correo": "sarah@gmail.com"
}'''
class ListarColaAPI(APIView): #funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        queue = DAOs.listarCola(correo)
        if queue:
            serializer = CancionSerializer(queue, many=True)
            return Response({'queue': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene cola de reproducción'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS CANCIONES DE UN ÁLBUM
{
    "nombreAlbum": "album de Sarah"
}'''
class ListarCancionesAlbumAPI(APIView): #funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombreAlbum = request.data.get('nombreAlbum')
        album = DAOs.conseguirAlbumPorNombre(nombreAlbum)
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
    def post(self, request):
        nombre = request.data.get('genero')
        genero = Genero(nombre=nombre)
        DAOs.crearGenero(genero)
        return Response({'message': 'Género creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR GÉNERO A UNA CANCIÓN
{
    "genero": "pop",
    "cancionId": "15"
}'''
class AgnadirGeneroAPI(APIView): # funciona # para canciones, hacer en el mismo para podcasts?
    permission_classes = [AllowAny]
    def post(self, request):
        generoNombre = request.data.get('genero')
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        genero = DAOs.conseguirGeneroPorNombre(generoNombre)
        DAOs.crearPertenecen(genero, cancion)
        return Response({'message': 'Género añadido con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR CANTANTE A UNA CANCIÓN
{
    "artista": "2",
    "cancionId": "15"
}'''
class AgnadirCantanteAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        artistaId = request.data.get('artista')
        cancionId = request.data.get('cancionId')
        artista = DAOs.conseguirArtistaPorId(artistaId)
        cancion = DAOs.conseguirCancionPorId(cancionId)
        DAOs.crearCantan(cancion, artista)
        return Response({'message': 'Cantante añadido con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LOS ARTISTAS DE UNA CANCIÓN
{
    "cancionId": "33"
}'''
class ListarArtistasCancionAPI(APIView): #funciona
    permission_classes = [AllowAny]
    def post(self, request):
        cancionId = request.data.get('cancionId')
        cancion = DAOs.conseguirCancionPorId(cancionId)
        artistas = DAOs.listarArtistasCancion(cancion)
        if artistas:
            serializer = ArtistaSerializer(artistas, many=True)
            return Response({'artistas': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay artistas en la canción'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS CANCIONES DE UN GÉNERO
{
    "genero": "Pop"
}'''
class FiltrarCancionesPorGeneroAPI(APIView): # funciona #quizás aprovechar para los capitulos
    permission_classes = [AllowAny]
    def post(self, request):
        genero = request.data.get('genero')
        canciones = DAOs.listarCancionesGenero(genero)
        if canciones:
            serializer = CancionSerializer(canciones, many=True)
            return Response({'canciones': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay canciones en ese género'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR PODCAST
{
    "nombre": "podcast1",
    "nombreFoto": "foto.jpg",
    
}''' 
class CrearPodcastAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        nombreFoto = request.data.get('nombreFoto')
        contenidoBinarioFoto = convertirBinario(nombreFoto)
        podcast = Podcast(nombre=nombre, puntuacion=0, numPuntuaciones=0, foto=contenidoBinarioFoto)
        DAOs.crearPodcast(podcast)
        return Response({'message': 'Podcast creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR PODCAST
{
    "podcastId": "2",
    "nombre": "podcast2",
    "presentadores": "arturo valls, patricia conde"
}'''
class ActualizarPodcastAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        podcastId = request.data.get('podcastId')
        nombre = request.data.get('nombre')
        presentadores = request.data.get('presentadores')
        podcast = Podcast(id=podcastId, nombre=nombre, presentadores=presentadores)
        DAOs.actualizarPodcast(podcast)
        return Response({'message': 'Podcast actualizado con éxito'}, status=status.HTTP_200_OK)

'''
EJEMPLO DE BUSCAR ARTISTA
{
    "artist_name": "Kanye West"
}

'''

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
            return Response({'message': 'Failed to obtain access token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
EJEMPLO DE BUSCAR
{
    "nombre": "a"
}'''
class BuscarAPI(APIView): #funciona, hay que conseguir que busque entre todo lo de debajo
    permission_classes = [AllowAny]
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
        if resultados:
            return Response(resultados, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No se han encontrado coincidencias'}, status=status.HTTP_404_NOT_FOUND)


class RecomendarAPI(APIView): #comprobar
    def post(self, request):
        correo = request.data.get('correo')
        #genero_id = request.data.get('genero_id') # esto sería que recomiende por género
        #artista_id = request.data.get('artista_id') # y por artista
        resultados = []

        generos_favoritos = DAOs.listarGenerosFavoritos(correo) # por hacer

        for genero in generos_favoritos:
            # obtener todas las canciones de ese género
            canciones_del_genero = Pertenecen.objects.filter(miGenero=genero).distinct()
            canciones_recomendadas = random.sample(list(canciones_del_genero), 3)
            for cancion in canciones_recomendadas:
                resultados.append(cancion)

        artistas_favoritos = DAOs.listarArtistasFavoritos(correo) # por hacer

        for artista in artistas_favoritos:
            # obtener todas las canciones de ese artista
            canciones_del_artista = Cantan.objects.filter(miArtista=artista).distinct()
            canciones_recomendadas = random.sample(list(canciones_del_artista), 3)
            for cancion in canciones_recomendadas:
                resultados.append(cancion)

        return resultados
        