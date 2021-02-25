from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import them_dau
from . import models
from tensorflow.keras.models import load_model
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
from django.http import HttpResponse
# Create your views here.

# Web API
# path = models.ModelThemDau.objects.get(id=1).model_h5.path
model = load_model('API/model.h5')


def them_daus(text):
    i = 0
    while len(text.split(' ')) < 5:
        text += ' 0226'
        i += 1
    text = them_dau.remove_accent(text)
    text = them_dau.add_accent(text, model)
    while ' 0226' in text:
        text = text.replace(' 0226', '')
    return text


def getResponse(question):
    data = json.dumps({"message": "%s" % question, "sender": "Me"})
    p = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      headers={"Content-Type": "application/json"}, data=data).json()
    print(p)
    try:
        return p[0]['text']
    except:
        return None


class Chatbot(APIView):

    def post(self, request):

        try:
            data = request.data
            text = data['text']
            text = them_daus(text)
            response = getResponse(text)
            if response is None:
                response = "Không hiểu"
            else:
                save_chat(text, response)
            return Response({'response': response, 'text': text}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Facebook API
PAGE_ACCESS_TOKEN = "EAALWsZArBpxcBAGQVJ4A7EjpilqGvoWGoIuK0ZBk7fHsO8sZCIVW9VLZCg0Ly6oocEj6eE8poYEOPR0rZBDFZCyfdC6FckViiLYtAPunZCxtHLKQKm7HpUDZCqM8okKb5ZA2qSZCQOPfcr54wRWjcmvkRCtLnDP5VIX8rzuLp6C4uTwwl7BZCpzlFX3"
VERIFY_TOKEN = "rasademo"


def post_facebook_message(fbid, recevied_message):
    recevied_message = them_daus(recevied_message)
    data = json.dumps({"message": "%s" % recevied_message, "sender": "Me"})
    p = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      headers={"Content-Type": "application/json"}, data=data).json()

    bot_res = p[0]['text']

    if bot_res is None:
        bot_res = "Không hiểu"
    else:
        save_chat(recevied_message, bot_res)

    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {
        'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}

    user_details = requests.get(user_details_url, user_details_params).json()

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN

    response_msg = json.dumps(
        {"recipient": {"id": fbid}, "message": {"text": bot_res}})
    status = requests.post(post_message_url, headers={
                           "Content-Type": "application/json"}, data=response_msg)


class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:

                if 'message' in message:
                    post_facebook_message(
                        message['sender']['id'], message['message']['text'])
        return HttpResponse()


def save_chat(user, bot):
    chat = models.Chat(chat_user=user, chat_bot=bot)
    chat.save()
