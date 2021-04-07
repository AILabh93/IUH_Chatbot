from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from . import serializers
from . import models
from account.serializers import SerializerUser
from rest_framework.decorators import api_view, permission_classes
# Create your views here.


class ViewPost(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        post = serializers.Serial_Post(
            instance=models.Post.objects.all(), many=True)
        return Response(data=post.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        post = models.Post.objects.create(
            user=request.user, title=data['title'], content=data['content'])
        serial_post = serializers.Serial_Post(post)
        post.save()
        return Response(data=serial_post.data, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data
        models.Post.objects.filter(pk=data['id']).update(
            title=data['title'], content=data['content'])

        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        models.Post.objects.filter(pk=request.data['id']).delete()
        return Response(status=status.HTTP_200_OK)


class Comment(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            post = models.Post.objects.get(pk=request.data['id_post'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comment = models.Comment.objects.create(
            post=post, user=request.user, content=request.data['content'])
        serial = serializers.Serial_Comment(comment)
        return Response(data=serial.data, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            models.Comment.objects.filter(pk=request.data['id']).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Reply(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            comment = models.Comment.objects.get(pk=request.data['id_cmt'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        reply = models.Reply.objects.create(
            comment=comment, user=request.user, content=request.data['content'])
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            models.Reply.objects.filter(pk=request.data['id']).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((AllowAny,))
def getDetail(request):
    id_post = request.GET['idpost']
    post = serializers.Serial_Post(
        instance=models.Post.objects.get(pk=id_post))
    return Response(data=post.data, status=status.HTTP_200_OK)
