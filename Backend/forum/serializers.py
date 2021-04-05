from rest_framework import serializers
from . import models


class Serial_Reply(serializers.ModelSerializer):

    class Meta:
        model = models.Reply
        fields = '__all__'


class Serial_Comment(serializers.ModelSerializer):
    reply = Serial_Reply(many=True, read_only=True)

    class Meta:
        model = models.Comment
        fields = '__all__'


class Serial_Post(serializers.ModelSerializer):
    comment = Serial_Comment(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = '__all__'
