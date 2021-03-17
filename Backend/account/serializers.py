from . import models
from rest_framework import serializers


class SerializerUser(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = '__all__'
