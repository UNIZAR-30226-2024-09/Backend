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
from Musify import views
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, viewsets
from .serializers import UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet,basename='userstest') #Esto son las "urls" de la api asi que habrá que traducir las vistas a datos en
                                            #formato serializado para poder atender las callas de la api, como en el del ejemplo
router.register(r'login', views.LoginAPIView,basename='login' )

router.register(r'register', views.UserRegistrationAPIView,basename='register' )
router.register(r'updateUser', views.UserUpdateAPIView,basename='updateUser' ) 
router.register(r'createArtist', views.CreateArtistAPIView,basename='createArtist' ) 







urlpatterns = [
    path('admin/', admin.site.urls),
    path('testFriends/', views.test_are_friends, name='test_are_friends'),
    path('testPlayList/', views.test_crear_playlist, name='test_crear_playlist'),
    path('testQueue/', views.test_queue_view, name='test_queue_view'),
    path('testPassword/', views.test_password_view, name='test_password_view'),
    path('testHistory1/', views.test_add_song_to_history, name='test_add_song_to_history'),
    path('testRemoveUser/', views.test_remove_user, name='test_remove_user'),
    path('testAddFriend/', views.test_add_friend, name='test_add_friend'),
    path('testRemoveFriend/', views.test_remove_friend, name='test_remove_friend'),
    path('testSong/', views.test_song, name='test_song'),
    path('testGenreSongs/', views.test_get_genre_songs, name='test_get_genre_songs'),
    path('testUpdateUser/', views.test_update_user, name='test_update_user'),
    path('testRemoveSongFromPlaylist/', views.test_remove_song_from_playlist, name='test_remove_song_from_playlist'),
    path('testRemoveSongFromHistory/', views.test_remove_song_from_history, name='test_remove_song_from_history'),
    path('removeSongFromQueue/', views.test_remove_song_from_queue, name='test_remove_song_from_queue'),
    path('testAlbum/', views.test_album, name='test_album'),
    #path('', include(router.urls)),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('updateUser/', views.UserUpdateAPIView.as_view(), name='updateUser'),
    path('createArtist/', views.CreateArtistAPIView.as_view(), name='createArtist'),
    ]
