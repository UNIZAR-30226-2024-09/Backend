"""
URL configuration for Psoft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from Musify import views, viewsChat
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, viewsets
from .serializers import UsuarioSerializer
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.views import LoginView
from Musify.backends import CorreoBackend
from Musify import consumers


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      #description="Test description",
      #terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@snippets.local"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
)

#ESTO SI HAY QUE DEJARLO, HABRÁ QUE CAMBIARLO A ESPAÑOL TAMBIÉN
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet,basename='userstest') #Esto son las "urls" de la api asi que habrá que traducir las vistas a datos en
                                            #formato serializado para poder atender las callas de la api, como en el del ejemplo
router.register(r'login', views.IniciarSesionAPI,basename='login' )

router.register(r'register', views.RegistroAPI,basename='register' )
#router.register(r'updateUser', views.ActualizarUsuarioAPI,basename='updateUser' ) 
router.register(r'createArtist', views.CrearArtistaAPI,basename='createArtist' ) 
router.register(r'createPlaylist', views.CrearPlaylistAPI,basename='createPlaylist' )
#router.register(r'updatePlaylistDetails', views.ActualizarPlaylistAPI, basename='updatePlaylistDetails')
router.register(r'addSongToPlaylist', views.AgnadirCancionPlaylistAPI,basename='addSongToPlaylist' )
router.register(r'removeSongFromPlaylist', views.EliminarCancionPlaylistAPI,basename='removeSongFromPlaylist' )
router.register(r'createSong', views.CrearCancionAPI,basename='createSong' )
router.register(r'addSongRating', views.PuntuarCancionAPI,basename='addSongRating' )
router.register(r'addSongToHistory', views.AgnadirCancionHistorialAPI,basename='addSongToHistory')
router.register(r'addSongToQueue', views.AgnadirCancionColaAPI,basename='addSongToQueue' )
router.register(r'removeSongFromQueue', views.EliminarCancionColaAPI,basename='removeSongFromQueue' )
router.register(r'createAlbum', views.CrearAlbumAPI,basename='createAlbum' )
router.register(r'addSongToAlbum', views.AgnadirCancionAlbumAPI,basename='addSongToAlbum' )
router.register(r'getHistory', views.ListarHistorialAPI,basename='getHistory' )

websocket_urlpatterns = [
    path('ws/chatroom/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('testFriends/', views.test_are_friends, name='test_are_friends'),
    #path('testPlayList/', views.test_crear_playlist, name='test_crear_playlist'),
    #path('testQueue/', views.test_queue_view, name='test_queue_view'),
    #path('testPassword/', views.test_password_view, name='test_password_view'),
    #path('testHistory1/', views.test_add_song_to_history, name='test_add_song_to_history'),
    #path('testRemoveUser/', views.test_remove_user, name='test_remove_user'),
    #path('testAddFriend/', views.test_add_friend, name='test_add_friend'),
    #path('testRemoveFriend/', views.test_remove_friend, name='test_remove_friend'),
    #path('testSong/', views.test_song, name='test_song'),
    #path('testGenreSongs/', views.test_get_genre_songs, name='test_get_genre_songs'),
    #path('testUpdateUser/', views.test_update_user, name='test_update_user'),
    #path('testRemoveSongFromPlaylist/', views.test_remove_song_from_playlist, name='test_remove_song_from_playlist'),
    #path('testRemoveSongFromHistory/', views.test_remove_song_from_history, name='test_remove_song_from_history'),
    #path('removeSongFromQueue/', views.test_remove_song_from_queue, name='test_remove_song_from_queue'),
    #path('testAlbum/', views.test_album, name='test_album'),
    #path('', include(router.urls)),
    path('iniciarSesion/', views.IniciarSesionAPI.as_view(), name='iniciarSesion'),
    path('registro/', views.RegistroAPI.as_view(), name='registro'),
    path('actualizarUsuario/', views.ActualizarUsuarioAPI.as_view(), name='actualizarUsuario'),
    path('eliminarUsuario/', views.EliminarUsuarioAPI.as_view(), name='eliminarUsuario'),
    #path('seguirAmigo/', views.SeguirAmigoAPI.as_view(), name='seguirAmigo'),
    #path('listarAmigos/', views.ListarAmigosAPI.as_view(), name='listarAmigos'),
    #path('dejarDeSeguirAmigo/', views.DejarDeSeguirAmigoAPI.as_view(), name='dejarDeSeguirAmigo'),
    #path('sonAmigos/', views.SonAmigosAPI.as_view(), name='sonAmigos'),
    path('seguir/', views.SeguirAPI.as_view(), name='seguir'),
    path('dejarDeSeguir/', views.DejarDeSeguirAPI.as_view(), name='dejarDeSeguir'),
    path('listarSeguidos/', views.ListarSeguidosAPI.as_view(), name='listarSeguidos'),
    path('listarSeguidores/', views.ListarSeguidoresAPI.as_view(), name='listarSeguidores'),
    path('crearPlaylist/', views.CrearPlaylistAPI.as_view(), name='crearPlaylist'),
    path('actualizarPlaylist/', views.ActualizarPlaylistAPI.as_view(), name='actualizarPlaylist'),
    path('crearArtista/', views.CrearArtistaAPI.as_view(), name='crearArtista'),
    path('listarHistorial/', views.ListarHistorialAPI.as_view(), name='listarHistorial'),
    path('agnadirCancionPlaylist/', views.AgnadirCancionPlaylistAPI.as_view(), name='agnadirCancionPlaylist'),
    path('eliminarCancionPlaylist/', views.EliminarCancionPlaylistAPI.as_view(), name='eliminarCancionPlaylist'),
    path('crearCancion/', views.CrearCancionAPI.as_view(), name='crearCancion'),
    path('puntuarCancion/', views.PuntuarCancionAPI.as_view(), name='puntuarCancion'),
    path('agnadirCancionCola/', views.AgnadirCancionColaAPI.as_view(), name='agnadirCancionCola'),
    path('eliminarCancionCola/', views.EliminarCancionColaAPI.as_view(), name='eliminarCancionCola'),
    path('crearAlbum/', views.CrearAlbumAPI.as_view(), name='crearAlbum'),
    path('actualizarAlbum/', views.ActualizarAlbumAPI.as_view(), name='actualizarAlbum'),
    path('agnadirCancionAlbum/', views.AgnadirCancionAlbumAPI.as_view(), name='agnadirCancionAlbum'),
    path('agnadirCancionHistorial/', views.AgnadirCancionHistorialAPI.as_view(), name='agnadirCancionHistorial'),
    path('crearPodcast/', views.CrearPodcastAPI.as_view(), name='crearPodcast'),
    path('crearCapitulo/', views.CrearCapituloAPI.as_view(), name='crearCapitulo'),
    path('actualizarCapitulo/', views.ActualizarCapituloAPI.as_view(), name='actualizarCapitulo'),
    path('crearGenero/', views.CrearGeneroAPI.as_view(), name='crearGenero'),
    path('agnadirGenero/', views.AgnadirGeneroAPI.as_view(), name='agnadirGenero'),
    path('crearPodcast/', views.CrearPodcastAPI.as_view(), name='crearPodcast'),
    path('actualizarPodcast/', views.ActualizarPodcastAPI.as_view(), name='actualizarPodcast'),
    path('listarCancionesPlaylist/', views.ListarCancionesPlaylistAPI.as_view(), name='listarCancionesPlaylist'),
    path('listarPlaylistsUsuario/', views.ListarPlaylistsUsuarioAPI.as_view(), name='listarPlaylistsUsuario'),
    path('listarCancionesAlbum/', views.ListarCancionesAlbumAPI.as_view(), name='listarCancionesAlbum'),
    path('listarCola/', views.ListarColaAPI.as_view(), name='listarCola'),
    path('listarCapitulosPodcast/', views.ListarCapitulosPodcastAPI.as_view(), name='listarCapitulosPodcast'),
    path('listarCanciones/', views.ListarCancionesAPI.as_view(), name='listarCanciones'),
    path('filtrarCancionesPorGenero/', views.FiltrarCancionesPorGeneroAPI.as_view(), name='filtrarCancionesPorGenero'),
    #path('buscarArtistaSPOTY/', views.BuscarArtistaSPOTY.as_view(), name='buscarArtistaSPOTY'),
    path('buscar/', views.BuscarAPI.as_view(), name='buscar'),
    path('listarPodcasts/', views.ListarPodcastsAPI.as_view(), name='listarPodcasts'),
    #path('google/login/', views.IniciarSesionConGoogleAPI.as_view(), name='iniciarSesionConGoogle'),
    #path('google/callback/', views.GoogleCallbackAPI.as_view(), name='googleCallback'),
    path('agnadirCantante/', views.AgnadirCantanteAPI.as_view(), name='agnadirCantante'),
    path('editarCancionFavoritos/', views.EditarCancionFavoritosAPI.as_view(), name='editarCancionFavoritos'),
    path('esFavorita/', views.EsFavoritaAPI.as_view(), name='esFavorita'),
    #path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('listarArtistasCancion/', views.ListarArtistasCancionAPI.as_view(), name='listarArtistasCancion'),
    path('crearPresentador/', views.CrearPresentadorAPI.as_view(), name='crearPresentador'),
    path('agnadirPresentador/', views.AgnadirPresentadorAPI.as_view(), name='agnadirPresentador'),
    path('listarPresentadoresPodcast/', views.ListarPresentadoresPodcastAPI.as_view(), name='listarPresentadoresPodcast'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('actualizarUsuarioNombre/', views.ActualizarUsuarioNombreAPI.as_view(), name='actualizarUsuarioNombre'),
    #path('actualizarUsuarioSexo/', views.ActualizarUsuarioSexoAPI.as_view(), name='actualizarUsuarioSexo'),
    #path('actualizarUsuarioNacimiento/', views.ActualizarUsuarioNacimientoAPI.as_view(), name='actualizarUsuarioNacimiento'),
    #path('actualizarUsuarioPais/', views.ActualizarUsuarioPaisAPI.as_view(), name='actualizarUsuarioPais'),
    #path('actualizarUsuarioContrasegna/', views.ActualizarUsuarioContrasegnaAPI.as_view(), name='actualizarUsuarioContrasegna'),
    #path('actualizarPlaylistNombre/', views.ActualizarPlaylistNombreAPI.as_view(), name='actualizarPlaylistNombre'),
    #path('actualizarPlaylistPublica/', views.ActualizarPlaylistPublicaAPI.as_view(), name='actualizarPlaylistPublica'),
    #path('actualizarAlbumNombre/', views.ActualizarAlbumNombreAPI.as_view(), name='actualizarAlbumNombre'),
    #path('actualizarAlbumFoto/', views.ActualizarAlbumFotoAPI.as_view(), name='actualizarAlbumFoto'),
    #path('actualizarCapituloNombre/', views.ActualizarCapituloNombreAPI.as_view(), name='actualizarCapituloNombre'),
    #path('actualizarCapituloDescripcion/', views.ActualizarCapituloDescripcionAPI.as_view(), name='actualizarCapituloDescripcion'),
    #path('actualizarCapituloPodcast/', views.ActualizarCapituloPodcastAPI.as_view(), name='actualizarCapituloPodcast'),
    #path('actualizarCapituloArchivo/', views.ActualizarCapituloArchivoAPI.as_view(), name='actualizarCapituloArchivo'),
    #path('actualizarPodcastNombre/', views.ActualizarPodcastNombreAPI.as_view(), name='actualizarPodcastNombre'),
    #path('actualizarPodcastFoto/', views.ActualizarPodcastFotoAPI.as_view(), name='actualizarPodcastFoto'),
    path('devolverCancion/', views.DevolverCancionAPI.as_view(), name='devolverCancion'),
    path('devolverAlbum/', views.DevolverAlbumAPI.as_view(), name='devolverAlbum'),
    path('devolverPlaylist/', views.DevolverPlaylistAPI.as_view(), name='devolverPlaylist'),
    path('devolverArtista/', views.DevolverArtistaAPI.as_view(), name='devolverArtista'),
    path('devolverPodcast/', views.DevolverPodcastAPI.as_view(), name='devolverPodcast'),
    path('devolverCapitulo/', views.DevolverCapituloAPI.as_view(), name='devolverCapitulo'),
    path('devolverUsuario/', views.DevolverUsuarioAPI.as_view(), name='devolverUsuario'),
    path('devolverPresentador/', views.DevolverPresentadorAPI.as_view(), name='devolverPresentador'),
    path('obtenerUsuarioSesionAPI/', views.ObtenerUsuarioSesionAPI.as_view(), name='ObtenerUsuarioSesionAPI'),
    path('cerrarSesionAPI/', views.CerrarSesionAPI.as_view(), name='CerrarSesionAPI'),
    path('actualizarEstadoCancionesAPI/', views.ActualizarEstadoCancionesAPI.as_view(), name='actualizarEstadoCancionesAPI'),
    path('obtenerEstadoCancionesAPI/', views.ObtenerEstadoCancionesAPI.as_view(), name='obtenerEstadoCancionesAPI'),
    path('agnadirColaboradorAPI/', views.AñadirColaboradorAPI.as_view(), name='agnadirColaboradorAPI'),
    path('reporteAPI/', views.ReporteAPI.as_view(), name='ReporteAPI'),
    path('eliminarPlaylistAPI/', views.EliminarPlaylistAPI.as_view(), name='EliminarPlaylistAPI'),
    path('registrarMensajeAPI/', viewsChat.RegistrarMensajeAPI.as_view(), name='RegistrarMensajeAPI'),
    path('cargarMensajesAPI/', viewsChat.CargarMensajesAPI.as_view(), name='CargarMensajesAPI'),
    path('crearSalaAPI/', viewsChat.CrearSalaAPI.as_view(), name='CrearSalaAPI'),
    path('siguiendo/', views.SiguiendoAPI.as_view(), name='Siguiendo'),
    ]
