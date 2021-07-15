from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import models
import json
import requests
from django.views import generic
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from . import sualoi
import os
import tensorflow as tf
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from . import serializers
import pickle
# Create your views here.
with open('API/models/token1.pkl', 'rb') as f:
    tokenizer_ipt, tokenizer_opt = pickle.load(f)

num_layers = 4
d_model = 256
dff = 512
num_heads = 8
ipt_vocab_size = tokenizer_ipt.vocab_size+2
opt_vocab_size = tokenizer_opt.vocab_size+2
dropout_rate = 0.2

transformer = sualoi.Transformer(num_layers=num_layers, d_model=d_model, num_heads=num_heads, dff=dff,
                                 input_vocab_size=ipt_vocab_size, target_vocab_size=opt_vocab_size,
                                 pe_input=ipt_vocab_size,
                                 pe_target=opt_vocab_size,
                                 rate=dropout_rate)
checkpoint_path = "API/models"

ckpt = tf.train.Checkpoint(transformer=transformer,)

ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)
if ckpt_manager.latest_checkpoint:
    ckpt.restore(ckpt_manager.latest_checkpoint)


def getResponse(question, state_change=True):
    """
        state_change: trang thai co sua loi hay khong
    """
    if state_change:
        question = sualoi.predict(
            question, tokenizer_ipt, tokenizer_opt, transformer, maxlen=150)
    data = json.dumps({"message": "%s" % question, "sender": "Me"})
    p = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      headers={"Content-Type": "application/json"}, data=data).json()

    return p, question


class Chatbot(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        question = data['text']
        response, questionC = getResponse(question, state_change=False)
        if len(response) == 0:
            response, questionC = getResponse(
                question, state_change=True)
        if len(response) == 0:
            response = 'Mình chưa hiểu ý bạn. Bạn hãy nói rõ hơn được không'
        else:
            response = response[0]['text']
        save_chat(questionC, response)
        return Response({'text_formated': questionC, 'response': response}, status=status.HTTP_200_OK)


# Facebook API
PAGE_ACCESS_TOKEN = "EAAK0AI5bxoQBAESZBmkPE2xWug0qvqcLHyZCkH8DWUO2a7nLA7VdVh8dQev6dHQ7eYS60hYdaVSZC8qZAnnuSKDZAkdMwXvY1RoEF5cjtr151dWQNXywfxjTxWllGgqaJ88bj9DzcBZA5v854C7aDy2jQO37DpQmi7XKi71ZC9f0QZDZD"
VERIFY_TOKEN = "rasademo"


def post_facebook_message(fbid, recevied_message, sua_loi=True):
    if sua_loi:
        recevied_message = sualoi.predict(recevied_message, tokenizer_ipt,
                                          tokenizer_opt, transformer)

        data = json.dumps({"message": "%s" % recevied_message, "sender": "Me"})
        p = requests.post('http://localhost:5005/webhooks/rest/webhook',
                          headers={"Content-Type": "application/json"}, data=data).json()
        if p is None:
            p = "Xin lỗi mình chưa hiều ý bạn"
        else:
            jsons = rasaToFbJson(p, fbid)
            save_chat(recevied_message, p)
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


@api_view(['GET'])
@permission_classes([AllowAny])
def getChat(request):
    chat = serializers.SerialChat(models.Chat.objects.all(), many=True)
    return Response(data=chat.data, status=status.HTTP_200_OK)


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
