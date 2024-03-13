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
    '''pertenecen_vo = Pertenecen(
        miGenero=genre_vo,
        miAudio=song_vo
    )'''
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



#TEST API
class UserViewSet(viewsets.ModelViewSet): #funciona
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer


        
'''EJEMPLO DE FORMATO JSON PARA LOGIN
{
    "username": "nerea@ejemplo.com",
    "password": "nerea"
}
'''

class LoginAPIView(APIView): #Utiliza formato json estandar(el de arriba) funciona
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(correo=username, password=password)

        if user is not None:
            # User is authenticated, return success response
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # Invalid credentials, return error response
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

'''EJEMPLO DE FORMATO JSON PARA REGISTRO
{
    "email": "john.doe@example.com",
    "name": "John Doe",
    "gender": "Male",
    "dateOfBirth": "1985-03-10",
    "password": "5U3rP@55w0rd",
    "country": "United States"
}
'''
import logging

logger = logging.getLogger(__name__)
class UserRegistrationAPIView(APIView): # funciona
    permission_classes = [AllowAny]

    def post(self, request):
        correo = request.data.get('email')
        nombre = request.data.get('name')
        sexo = request.data.get('gender')
        nacimiento = request.data.get('dateOfBirth')
        contrasegna = request.data.get('password')
        pais = request.data.get('country')

        if not nombre:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f'Nombre recibido: {nombre}')

        user = Usuario(correo=correo, nombre=nombre, sexo=sexo, nacimiento=nacimiento, contrasegna=contrasegna, pais=pais)

        if Usuario.objects.filter(correo=correo).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        DAOs.create_user(user)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_200_OK)

'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR USUARIO (igual que el de register)'''

class UserUpdateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        sexo = request.data.get('sexo')
        nacimiento = request.data.get('nacimiento')
        contrasegna = request.data.get('contrasegna')
        pais = request.data.get('pais')
        user = Usuario(correo=correo, nombre=nombre, sexo=sexo, nacimiento=nacimiento, contrasegna=contrasegna, pais=pais)
        DAOs.update_user(user)
        return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)

class UserDeleteAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        DAOs.remove_user(correo)
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)

class FriendAdditionAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        amigo = request.data.get('amigo')
        DAOs.add_friend(correo, amigo)
        return Response({'message': 'Friend added successfully'}, status=status.HTTP_200_OK) 
    
class GetFriendsAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email') # coger el correo de la sesión
        friends = DAOs.get_friends(correo)
        if friends != None:
            return Response({'friends': friends}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene amigos'}, status=status.HTTP_200_OK)


class RemoveFriendAPIView(APIView): 
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        amigo = request.data.get('amigo')
        DAOs.remove_friend(correo, amigo)
        return Response({'message': 'Friend removed successfully'}, status=status.HTTP_200_OK)
    
class AreFriendsAPIView(APIView): #Work as expected
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        amigo = request.data.get('amigo')
        if DAOs.are_friends(correo, amigo) == True:
            return Response({'message': 'Son amigos'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No son amigos'}, status=status.HTTP_200_OK)
            
class CreatePlaylistAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        privada = request.data.get('privada')
        if Colabora.objects.filter(miUsuario=correo, miPlaylist=nombre).exists():
            return Response({'error': 'Playlist already exists'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.create_playlist(correo, nombre, privada)
        return Response({'message': 'Playlist created successfully'}, status=status.HTTP_200_OK)

class UpdatePlaylistDetailsAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        id_playlist = request.data.get('id_playlist')
        nombre = request.data.get('nombre')
        publica = request.data.get('publica')
        DAOs.update_playlist_details(id_playlist, nombre, publica)
        return Response({'message': 'Playlist updated successfully'}, status=status.HTTP_200_OK)

class GetSongsFromPlaylistAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email')
        # ACABAR

class AddSongToPlaylistAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        id_playlist = request.data.get('id_playlist')
        id_cancion = request.data.get('id_cancion')
        if Contiene.objects.filter(miAudio=id_cancion, miPlaylist=id_playlist).exists():
            return Response({'error': 'Song already exists in playlist'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.add_song_to_playlist(id_playlist, id_cancion)
        return Response({'message': 'Song added to playlist successfully'}, status=status.HTTP_200_OK)

class RemoveSongFromPlaylistAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        id_playlist = request.data.get('id_playlist')
        id_cancion = request.data.get('id_cancion')
        if not Contiene.objects.filter(miAudio=id_cancion, miPlaylist=id_playlist).exists():
            return Response({'error': 'Song does not exist in playlist'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.remove_song_from_playlist(id_playlist, id_cancion)
        return Response({'message': 'Song removed from playlist successfully'}, status=status.HTTP_200_OK)

class GetPlaylistsFromUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email') # coger el correo de la sesión
        playlists = DAOs.get_playlists_from_user(correo)
        if playlists != None:
            return Response({'playlists': playlists}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene playlists'}, status=status.HTTP_200_OK)


# aquí falta el atributo cantantes
class CreateSongAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        miAlbum = request.data.get('miAlbum')
        puntuacion = request.data.get('puntuacion')
        cancion = Cancion(nombre=nombre, miAlbum=miAlbum, puntuacion=puntuacion)
        DAOs.create_song(cancion)
        return Response({'message': 'Song created successfully'}, status=status.HTTP_200_OK)

class AddSongRatingAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        id_cancion = request.data.get('id_cancion')
        puntuacion = request.data.get('puntuacion')
        DAOs.add_song_rating(id_cancion, puntuacion)
        return Response({'message': 'Song rating added successfully'}, status=status.HTTP_200_OK)




class AddSongToQueueAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        id_cancion = request.data.get('id_cancion')
        DAOs.add_song_to_queue(correo, id_cancion)
        return Response({'message': 'Song added to queue successfully'}, status=status.HTTP_200_OK)

class RemoveSongFromQueueAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        id_cancion = request.data.get('id_cancion')
        if not Cola.objects.filter(miUsuario=correo, miAudio=id_cancion).exists():
            return Response({'error': 'Song does not exist in queue'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.remove_song_from_queue(correo, id_cancion)
        return Response({'message': 'Song removed from queue successfully'}, status=status.HTTP_200_OK)

# no se si está bien
class CreateAlbumAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        album = Album(nombre=nombre)
        DAOs.create_album(album)
        return Response({'message': 'Album created successfully'}, status=status.HTTP_200_OK)

# no se si está bien
class AddSongToAlbumAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombre_album = request.data.get('nombre_album')
        album = DAOs.get_album_by_name(nombre_album)
        nombre_cancion = request.data.get('nombre_cancion')
        cancion = DAOs.get_song_by_name(nombre_cancion)
        if Cancion.objects.filter(nombre=nombre_cancion, miAlbum=album).exists():
            return Response({'message': 'Song is already in album'}, status=status.HTTP_400_BAD_REQUEST)
        DAOs.add_song_to_album(album, cancion)
        return Response({'message': 'Song added to album successfully'}, status=status.HTTP_200_OK)

# sin acabar
class CreateEpisodeAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        miPodcast = request.data.get('miPodcast')

'''EJEMPLO DE FORMATO JSON PARA CREAR ARTISTA
{
    "nombre": "Kanye West",
    "descripcion": "Kanye West descrption here..."
}
'''
class CreateArtistAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        artista = Artista(nombre=nombre, descripcion=descripcion)
        DAOs.create_artist(artista)
        return Response({'message': 'Artist created successfully'}, status=status.HTTP_200_OK)
    
class GetUserHistoryAPIView(APIView): 
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email') # coger el correo de la sesión
        history = DAOs.get_user_history(correo)
        if history != None:
            return Response({'history': history}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene historial'}, status=status.HTTP_200_OK)

class AddSongToHistoryAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email') # coger el correo de la sesión
        cancion_nombre = request.data.get('cancion_nombre') # coger el nombre de la cancion
        cancion = DAOs.get_song_by_name(cancion_nombre)
        DAOs.add_song_to_history(correo, cancion)
        return Response({'message': 'Song added to history successfully'}, status=status.HTTP_200_OK)
    
# lo hacemos???
#class RemoveSongFromHistoryAPIView(APIView):

class GetUserQueueAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('email') # coger el correo de la sesión
        queue = DAOs.get_queue_from_user(correo)
        if queue != None:
            return Response({'queue': queue}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene cola de reproducción'}, status=status.HTTP_200_OK)

class GetAlbumSongsAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        nombreAlbum = request.data.get('nombreAlbum')
        album = DAOs.get_album_by_name(nombreAlbum)
        songs = DAOs.get_album_songs(album)
        if songs != None:
            return Response({'songs': songs}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay canciones en el álbum'}, status=status.HTTP_200_OK)    