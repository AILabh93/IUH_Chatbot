from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.response import Response
from . import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

User = get_user_model()


# class tao (post) va dang nhap(get)
class Profile(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        user = request.GET
        auth = authenticate(
            username=user['username'], password=user['password'])

        if auth is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        se = serializers.SerializerUser(
            User.objects.get(username=user['username']))
        token = TokenObtainPairSerializer().get_token(user=auth)
        data = {
            'refresh_token': str(token),
            'access_token': str(token.access_token),
            'user': se.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):

        data = request.data
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                avatar=data['avatar'],
                full_name=data['full_name']
            )
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(data={'error': 'tài khoản đã tồn tại'}, status=status.HTTP_400_BAD_REQUEST)


# update user
@api_view(['POST', ])
def updateUser(request):
    serializer = serializers.SerializerUser(
        request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


# check login
@api_view(['GET', ])
def chech_login(request):
    serializer = serializers.SerializerUser(request.user)
    if serializer is not None:
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# get all user using token of admin
# if it is not admin then function will response http 403
# if not send token return http 401
@api_view(['GET', ])
@permission_classes((IsAdminUser, ))
def getAllUser(request):
    user = serializers.SerializerUser(instance=User.objects.all(), many=True)
    return Response(data=user.data, status=status.HTTP_200_OK)
