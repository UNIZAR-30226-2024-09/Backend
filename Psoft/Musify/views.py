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
class UserViewSet(viewsets.ModelViewSet): #Works as expected
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer

'''EJEMPLO DE FORMATO JSON PARA LOGIN
{
    "username": "nerea@ejemplo.com",
    "password": "nerea"
}
'''

class LoginAPIView(APIView): #Utiliza formato json estandar(el de arriba)
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
    "correo": "john.doe@example.com",
    "nombre": "John Doe",
    "sexo": "Male",
    "nacimiento": "1985-03-10",
    "contrasegna": "5U3rP@55w0rd",
    "pais": "United States"
}
'''
class UserRegistrationAPIView(APIView): #Works as expected
    permission_classes = [AllowAny]
    def post(self, request):
        correo = request.data.get('correo')
        nombre = request.data.get('nombre')
        sexo = request.data.get('sexo')
        nacimiento = request.data.get('nacimiento')
        contrasegna = request.data.get('contrasegna')
        pais = request.data.get('pais')
        user = Usuario.objects.create(correo=correo, nombre=nombre, sexo=sexo, nacimiento=nacimiento, contrasegna=contrasegna, pais=pais)
        # Check if the username is already taken
        if Usuario.objects.filter(correo=correo).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        DAOs.create_user(user)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
'''EJEMPLO DE FORMATO JSON PARA ACTUALIZAR USUARIO (igual que el de register)'''

class UserUpdateAPIView(APIView): #Work as expected
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
        return Response({'message': 'User updated successfully'}, status=status.HTTP_201_CREATED)
    

'''EJEMPLO DE FORMATO JSON PARA CREAR ARTISTA
{
    "nombre": "Kanye West",
    "descripcion": "Kanye West descrption here..."
}
'''
class CreateArtistAPIView(APIView): #Work as expected
    permission_classes = [AllowAny]
    def post(self, request):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        artista = Artista(nombre=nombre, descripcion=descripcion)
        DAOs.create_artist(artista)
        return Response({'message': 'Artist created successfully'}, status=status.HTTP_201_CREATED)