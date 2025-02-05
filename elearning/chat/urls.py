
from django.urls import path
from .views import global_chat_room

app_name = 'chat'

urlpatterns = [
    path('', global_chat_room, name='global-chat-room'),
]