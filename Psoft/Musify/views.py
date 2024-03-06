from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Usuario, Amigo, Cancion, Podcast, Capitulo, Playlist, Colabora, Contiene, Historial, Favorito, Cola, Genero, Pertenecen, Album
from . import DAOs
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

# MAL
def test_add_song_to_history(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    song_vo = DAOs.get_song_by_id(7)
    DAOs.add_song_to_history(user_vo.correo, song_vo.id)
    history = DAOs.get_user_history("Paco@gmail.com")
    if history != None:
        for song in history:
            print(song.nombre + "\n")
    else :
        print("No hay canciones en el historial")
    return HttpResponse(status=200)

# MAL
def test_remove_user(request):
    nuevo_usuario = Usuario(
        correo='ejemplo@gmail.com',
        nombre='ej',
        sexo='',
        nacimiento=timezone.now(),
        contrasegna='ej',
        pais=''
    )
    DAOs.create_user(nuevo_usuario)
    DAOs.remove_user(nuevo_usuario.correo)
    if DAOs.get_user_by_correo("ejemplo@gmail.com") == None:
        print("Usuario eliminado")
    else:
        print("Usuario no eliminado")
    return HttpResponse(status=200)


def test_add_friend(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    nuevo_amigo = Usuario(
        correo='PacoAmigo2@gmail.com',
        nombre='PacoAmigo2',
        sexo='',
        nacimiento='',
        contrasegna='PacoAmigo2',
        pais=''
    )
    #DAOs.create_user(nuevo_amigo)
    nuevo_amigo = DAOs.get_user_by_correo("pacoamigo2@gmail.com")
    DAOs.add_friend(user_vo.correo, nuevo_amigo.correo)
    friends = DAOs.get_friends(user_vo.correo)
    print("Amigos de Paco: ")
    for friend in friends:
        print(friend.correo + "\n")
    return HttpResponse(status=200)

def test_song(request):
    nueva_cancion = Cancion(
        letra='letra',
        cantantes='cantantes',
        miAlbum=None,
        puntuacion=None,
        nombre="Cancion de ejemplo"
    )
    DAOs.create_song(nueva_cancion)
    DAOs.add_song_to_playlist(1, DAOs.get_song_by_name("Cancion de ejemplo").id)
    Canciones = DAOs.get_songs_from_playlist(1)
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
            DAOs.add_song_rating(DAOs.get_song_by_name("Cancion de ejemplo").id, 5)
            print(DAOs.get_song_rating(DAOs.get_song_by_name("Cancion de ejemplo").id))
            #print(DAOs.get_song_album(DAOs.get_song_by_name("Cancion de ejemplo").id))
            print(DAOs.get_song_artists(DAOs.get_song_by_name("Cancion de ejemplo").id))
    return HttpResponse(status=200)     



def test_remove_friend(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    nuevo_amigo = DAOs.get_user_by_correo("pacoamigo2@gmail.com")
    DAOs.remove_friend(user_vo.correo, nuevo_amigo.correo)
    return HttpResponse(status=200)

def test_get_genre_songs(request):
    DAOs.create_genre('pop')
    song_vo=DAOs.get_song_by_id(7)
    pertenecen_vo = Pertenecen(
        miGenero='pop',
        miAudio=song_vo.id
    )
    songs=DAOs.get_genre_songs('pop')
    for song in songs:
        print(song.nombre + "\n")
    return HttpResponse(status=200)

