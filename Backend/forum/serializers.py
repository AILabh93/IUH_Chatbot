from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Serial_Comment(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class Serial_User(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class Serial_Post(serializers.ModelSerializer):
    comment = Serial_Comment(many=True, read_only=True)
    user = Serial_User()

    class Meta:
        model = models.Post
        fields = '__all__'
