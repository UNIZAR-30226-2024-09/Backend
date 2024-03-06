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
from django.urls import path

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
    path('', views.home, name='home')
]