from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.response import Response
from . import serializers

# Create your views here.

User = get_user_model()


class Profile(APIView):

    def get(self, request):
        user = request.data
        auth = authenticate(
            username=user['username'], password=user['password'])

        if auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        se = serializers.SerializerUser(
            User.objects.get(username=user['username']))
        return Response(data=se.data, status=status.HTTP_200_OK)

    def post(self, request):

        data = request.data
        print(data)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            avatar=data['avatar'],
            full_name=data['full_name']
        )
        user.save()
        return Response(status=status.HTTP_200_OK)
