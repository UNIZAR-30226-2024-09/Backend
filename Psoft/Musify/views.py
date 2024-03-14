from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Usuario, Amigo, Cancion, Podcast, Capitulo, Playlist, Colabora, Contiene, Historial, Favorito, Cola, Genero, Pertenecen, Album, Artista
from . import DAOs
from Psoft.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

# VISTAS DE PRUEBA
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
    serializer_class = UserSerializer


        
'''EJEMPLO DE FORMATO JSON PARA INICIAR SESION
{
    "correo": "nerea@ejemplo.com",
    "contrasegna": "nerea"
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
            return Response({'message': 'Inicio de sesión correcto'}, status=status.HTTP_200_OK)
        else:
            # El usuario no ha sido autenticado, devolver respuesta de error
            return Response({'error': 'Correo o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)

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

        if not nombre:
            return Response({'error': 'Nombre es un campo obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f'Nombre recibido: {nombre}')

        user = Usuario(correo=correo, nombre=nombre, sexo=sexo, nacimiento=nacimiento, contrasegna=contrasegna, pais=pais)

        if Usuario.objects.filter(correo=correo).exists():
            return Response({'error': 'El correo introducido ya tiene asociada una cuenta'}, status=status.HTTP_400_BAD_REQUEST)

        DAOs.crearUsuario(user)
        return Response({'message': 'Usuario registrado con éxito'}, status=status.HTTP_200_OK)

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
    
class ListarAmigosAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        amigos = DAOs.listarAmigos(correo)
        if amigos != None:
            return Response({'amigos': amigos}, status=status.HTTP_200_OK)
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
            if Colabora.objects.filter(miUsuario=correo, miPlaylist=DAOs.get_playlist_by_name(nombre).id).exists():
                    return Response({'error': 'La playlist ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            DAOs.crearPlaylist(correo, nombre, publica)
            return Response({'message': 'La playlist se ha creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR UNA PLAYLIST
{
    "id_playlist": "2",
    "nombre": "Playlist de Sarah",
    "publica": "False"
}'''

class ActualizarPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        id_playlist = request.data.get('id_playlist')
        nombre = request.data.get('nombre')
        publica = request.data.get('publica')
        DAOs.actualizarPlaylist(id_playlist, nombre, publica)
        return Response({'message': 'La playlist ha sido actualizada con éxito'}, status=status.HTTP_200_OK)

class ListarCancionesDePlaylistAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        playlist = request.data.get('playlist') # de dónde se coge la playlist?
        # habría que mirar la tabla Colabora tmb?
        canciones = DAOs.listarCancionesPlaylist(playlist.id)
        if canciones != None:
            return Response({'songs': canciones}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'La playlist no tiene canciones'}, status=status.HTTP_200_OK)
        
        # ACABAR
'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN A UNA PLAYLIST
{
    "id_playlist": "2",
    "id_cancion": "26"
}'''

class AgnadirCancionPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        #correo = request.data.get('email') # coger correo de la sesión
        id_playlist = request.data.get('id_playlist')
        id_cancion = request.data.get('id_cancion')
        if Contiene.objects.filter(miAudio=id_cancion, miPlaylist=id_playlist).exists():
            return Response({'error': 'La canción ya está en la playlist'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.agnadirCancionPlaylist(id_playlist, id_cancion)
        return Response({'message': 'La canción ha sido añadida con éxito a la playlist'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ELIMINAR UNA CANCIÓN DE UNA PLAYLIST
{
    "id_playlist": "2",
    "id_cancion": "26"
}'''

class EliminarCancionPlaylistAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        id_playlist = request.data.get('id_playlist')
        id_cancion = request.data.get('id_cancion')
        if not Contiene.objects.filter(miAudio=id_cancion, miPlaylist=id_playlist).exists():
            return Response({'error': 'La canción no existe en la playlist'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.eliminarCancionPlaylist(id_playlist, id_cancion)
        return Response({'message': 'La canción ha sido eliminada con éxito de la playlist'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS PLAYLISTS DE UN USUARIO
{
    "correo": "john.doe@example.com"
}
'''
class ListarPlaylistsDeUsuarioAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        playlists = DAOs.listarPlaylistsUsuario(correo)
        if playlists != None:
            return Response({'playlists': playlists}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene playlists'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR CANCIÓN
{
    "nombre": "Buenas tardes",
    "miAlbum": "album de Paco5",
    "puntuacion": "5"
}'''

# aquí falta el atributo cantantes
class CrearCancionAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        miAlbum = request.data.get('miAlbum')
        puntuacion = request.data.get('puntuacion')
        miAlbum = DAOs.get_album_by_name(miAlbum)
        cancion = Cancion(nombre=nombre, miAlbum=miAlbum, puntuacion=puntuacion)
        DAOs.crearCancion(cancion)
        return Response({'message': 'Canción creada con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA PUNTUAR UNA CANCIÓN
{}
    "id_cancion": "27",
    "puntuacion": "4"
}'''

class PuntuarCancionAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        id_cancion = request.data.get('id_cancion')
        puntuacion = request.data.get('puntuacion')
        DAOs.puntuarCancion(id_cancion, puntuacion)
        return Response({'message': 'Canción puntuada con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN A LA COLA DE REPRODUCCIÓN
{
    "correo": "sarah@gmail.com",
    "id_cancion": "27"
}'''

class AgnadirCancionColaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        id_cancion = request.data.get('id_cancion')
        DAOs.add_song_to_queue(correo, id_cancion)
        return Response({'message': 'Canción añadida a la cola de reproducción con éxito'}, status=status.HTTP_200_OK)

class EliminarCancionColaAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        id_cancion = request.data.get('id_cancion')
        if not Cola.objects.filter(miUsuario=correo, miAudio=id_cancion).exists():
            return Response({'error': 'La canción no existe en la cola de reproducción'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.remove_song_from_queue(correo, id_cancion)
        return Response({'message': 'Canción eliminada de la cola de reproducción con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR ÁLBUM
{
    "nombre": "album de Sarah"
}'''

# no se si está bien
class CrearAlbumAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        album = Album(nombre=nombre)
        DAOs.create_album(album)
        return Response({'message': 'Álbum creado con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR AÑADIR CANCIÓN A UN ÁLBUM
{
    "nombre_album": "album de Sarah",
    "nombre_cancion": "Buenas tardes"
}'''

class AgnadirCancionAlbumAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        nombre_album = request.data.get('nombre_album')
        album = DAOs.get_album_by_name(nombre_album)
        nombre_cancion = request.data.get('nombre_cancion')
        cancion = DAOs.get_song_by_name(nombre_cancion)
        if Cancion.objects.filter(nombre=nombre_cancion, miAlbum=album).exists():
            return Response({'message': 'La cancion ya existe está en el álbum'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.add_song_to_album(album, cancion)
        return Response({'message': 'Canción añadida al álbum con éxito'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR CAPITULO
{
    "nombre": "episodio1",
    "descripcion": "descripcion del epidodio1"
    "miPodcast": "podcast de Sarah" 
}'''
# se tiene que hacer primero createPodcast
# sin acabar
class CrearCapituloAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        miPodcast = request.data.get('miPodcast')
        if not nombre:
            return Response({'error': 'Nombre es un campo obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f'Nombre recibido: {nombre}')

        DAOs.create_episode(nombre, descripcion, miPodcast)
        return Response({'message': 'Capítulo almacenado correctamente'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA CREAR ARTISTA
{
    "nombre": "Kanye West",
    "descripcion": "Kanye West descrption here..."
}
'''
class CrearArtistaAPI(APIView):
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

class ListarHistorialAPI(APIView): 
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo') # coger el correo de la sesión
        history = DAOs.get_user_history(correo)
        if history != None:
            return Response({'history': history}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene historial'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA AÑADIR UNA CANCIÓN AL HISTORIAL DE UN USUARIO
{
    "correo": "sarah@gmail.com"
    "cancion_nombre": "Buenas tardes"
}'''

class AgnadirCancionHistorialAPI(APIView): # funciona
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email') # coger el correo de la sesión
        cancion_nombre = request.data.get('cancion_nombre') # coger el nombre de la cancion
        cancion = DAOs.get_song_by_name(cancion_nombre)
        DAOs.add_song_to_history(correo, cancion)
        return Response({'message': 'Canción añadida al historial con éxito'}, status=status.HTTP_200_OK)
    
# lo hacemos???
#class EliminarCancionHistorialAPI(APIView):
    
'''EJEMPLO DE FORMATO JSON PARA LISTAR LA COLA DE REPRODUCCIÓN DE UN USUARIO
{
    "correo": "sarah@gmail.com"
}'''
class ListarColaAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email') # coger el correo de la sesión
        queue = DAOs.get_queue_from_user(correo)
        if queue != None:
            return Response({'queue': queue}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene cola de reproducción'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA LISTAR LAS CANCIONES DE UN ÁLBUM
{
    "nombreAlbum": "album de Sarah"
}'''
class ListarCancionesAlbumAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombreAlbum = request.data.get('nombreAlbum')
        album = DAOs.get_album_by_name(nombreAlbum)
        canciones = DAOs.get_album_songs(album)
        if canciones != None:
            return Response({'songs': canciones}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay canciones en el álbum'}, status=status.HTTP_200_OK)    