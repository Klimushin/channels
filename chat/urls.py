from django.urls import path

from chat.views import index, room

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    # path('', Index.as_view(), name='index'),
    path('<str:room_name>/', room, name='room'),
]
