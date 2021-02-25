from django.urls import path
from . import views
urlpatterns = [
    path('get-response/', views.Chatbot.as_view()),
    path('fb-rasa/', views.BotView.as_view())
]
