from django.urls import path
from . import views

urlpatterns = [
    path('create-user/', views.createUser),
    path('login/', views.logIn),
    path('update/', views.updateUser),
    path('check-login/', views.chech_login),
    path('get-all/', views.getAllUser)
]
