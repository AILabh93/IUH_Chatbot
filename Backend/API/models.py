from django.db import models

# Create your models here.


class Chat(models.Model):
    chat_user = models.TextField(max_length=200)
    chat_bot = models.TextField(max_length=200)
