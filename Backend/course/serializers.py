from . import models
from rest_framework import serializers


class Serial_Course(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'
