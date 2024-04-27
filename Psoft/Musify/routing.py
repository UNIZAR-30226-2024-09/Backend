from django.urls import path
from . import views

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', views.ChatConsumer.as_asgi()),
]