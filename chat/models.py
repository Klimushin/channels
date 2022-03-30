from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.db import models
from django.conf import settings


# Create your models here.
# User = get_user_model()


class ChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    # content = models.TextField()

    def __str__(self):
        return self.content

    def last_10_massages(self):
        return ChatMessage.objects.order_by('-timestamp').all()[:10]


class ChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    participants = models.ManyToManyField(ChatUser, )
    massages = models.ManyToManyField(ChatMessage, blank=True)

    def __str__(self):
        return self.title
