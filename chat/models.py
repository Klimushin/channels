from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()



class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_massages(self):
        return Message.objects.order_by('-timestamp').all()[:10]


# class ChatRoom(models.Model):
#     title = models.CharField(max_length=255, unique=True, blank=False)
#     participants = models.ManyToManyField(ChatUser, )
#     massages = models.ManyToManyField(ChatMessage, blank=True)
#
#     def __str__(self):
#         return self.title
