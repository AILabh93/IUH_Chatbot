from django.shortcuts import render
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core import serializers as seri
import json
from rest_framework.decorators import api_view
# Create your views here.


class ViewCourse(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        '''
            get all courses in database
        '''
        course = serializers.Serial_Course(
            models.Course.objects.all(), many=True)
        return Response(data=course.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
            Add course to database
        '''
        course = serializers.Serial_Course(data=request.data)
        if course.is_valid():
            course.save()
            return Response(course.data, status=status.HTTP_200_OK)
        return Response(course.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        '''
            Update course using id
        '''
        serializers.Serial_Course().update(
            models.Course.objects.get(pk=request.data['id']), request.data)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        '''
            delete course using id
        '''
        models.Course.objects.filter(pk=request.data['id']).delete()
        return Response(status=status.HTTP_200_OK)
