from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_room, name='chat_room'),
    path('room/<str:channel_code>/', views.chat_room, name='chat_room_detail'),
    path('agent/workspace/', views.agent_workspace, name='agent_workspace'),
    path('api/send/<str:channel_code>/', views.api_send_message, name='api_send_message'),
    path('api/poll/<str:channel_code>/', views.api_poll_messages, name='api_poll_messages'),
]
