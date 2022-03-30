from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

# class Index(TemplateView):
#     template_name = 'chat/index.html'
