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
from rest_framework.permissions import AllowAny
from . import sua_loi
# Create your views here.


model = load_model('API/models/model_sua_loi.h5')
#model_add = load_model('API/models/model.h5')


def sua(text):
    current_text = text
    current_len = len(text.split())

    i = 0
    while len(text.split(' ')) < 5:
        text += ' 0226'
        i += 1

    text = sua_loi.correct(text, model)
    # text = them_dau.remove_accent(text)
    # text = them_dau.accent_sentence(text, model_add)
    try:
        return ' '.join(text.split()[i] for i in range(current_len))
    except:
        return current_text


def getResponse(question):
    data = json.dumps({"message": "%s" % question, "sender": "Me"})
    p = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      headers={"Content-Type": "application/json"}, data=data).json()
    print(p)
    try:
        p[0]['text']
        return p
    except:
        return None


class Chatbot(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        try:
            data = request.data
            text = data['text']
            text = sua(text)
            response = getResponse(text)
            if response is None:
                response = "Không hiểu"
            else:
                response = response[0]['text']
                # save_chat(text, response)
            return Response({'text_formated': text, 'response': response}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Facebook API
PAGE_ACCESS_TOKEN = "EAAK0AI5bxoQBAESZBmkPE2xWug0qvqcLHyZCkH8DWUO2a7nLA7VdVh8dQev6dHQ7eYS60hYdaVSZC8qZAnnuSKDZAkdMwXvY1RoEF5cjtr151dWQNXywfxjTxWllGgqaJ88bj9DzcBZA5v854C7aDy2jQO37DpQmi7XKi71ZC9f0QZDZD"
VERIFY_TOKEN = "rasademo"


def post_facebook_message(fbid, recevied_message, sua_loi=True):
    if sua_loi:
        recevied_message = sua(recevied_message)

        data = json.dumps({"message": "%s" % recevied_message, "sender": "Me"})
        p = requests.post('http://localhost:5005/webhooks/rest/webhook',
                          headers={"Content-Type": "application/json"}, data=data).json()

        if p is None:
            p = "Không hiểu"
        else:
            jsons = rasaToFbJson(p, fbid)
            # save_chat(recevied_message, bot_res)
        send(fbid, jsons)
        return
    json_file = {
        "recipient": {
            "id": fbid
        },
        "message": {
            "text": recevied_message
        }
    }
    send(fbid, json_file)


def send(fbid, json_file):
    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {
        'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}

    user_details = requests.get(user_details_url, user_details_params).json()

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN

    response_msg = json.dumps(json_file)
    status = requests.post(post_message_url, headers={
                           "Content-Type": "application/json"}, data=response_msg)


class BotView(generic.View):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                print(message)
                if 'message' in message:
                    try:
                        post_facebook_message(
                            message['sender']['id'], message['message']['text'])
                    except:
                        post_facebook_message(
                            message['sender']['id'], ":D :D", sua_loi=False)
                if 'postback' in message:
                    post_facebook_message(
                        message['sender']['id'], message['postback']['payload'])
        return HttpResponse()


def save_chat(user, bot):
    chat = models.Chat(chat_user=user, chat_bot=bot)
    chat.save()


def rasaToFbJson(rasa, idfb):
    jsons = {
        "recipient": {
            "id": idfb
        },
        "message": {
        }
    }
    if len(rasa) > 1:
        if 'buttons' in rasa[1]:
            buttons = rasa[1]['buttons']
            jsons["message"]["attachment"] = {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": rasa[0]['text'],
                    "buttons": [
                        {
                            "type": "postback",
                            "title": buttons[0]['title'],
                            "payload": buttons[0]['payload']
                        },
                        {
                            "type": "postback",
                            "title": buttons[1]['title'],
                            "payload": buttons[1]['payload']
                        },
                        {
                            "type": "postback",
                            "title": buttons[2]['title'],
                            "payload": buttons[2]['payload']
                        },
                        # {
                        #     "type": "postback",
                        #     "title": buttons[3]['title'],
                        #     "payload": buttons[3]['payload']
                        # },
                        # {
                        #     "type": "postback",
                        #     "title": buttons[4]['title'],
                        #     "payload": buttons[4]['payload']
                        # }
                    ]
                }
            }
        else:
            jsons["message"]["attachment"] = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": 'Lương',
                            "image_url": rasa[1]['image'],
                            "subtitle": rasa[0]['text'],

                        }
                    ]}}
    else:
        jsons["message"]["text"] = rasa[0]['text']
    return jsons
