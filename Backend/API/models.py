from django.db import models
from mongoengine import Document, fields
# Create your models here.


class Chat(models.Model):
    chat_user = models.CharField(max_length=200)
    chat_bot = models.CharField(max_length=200)
