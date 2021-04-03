from django.urls import path
from . import views

urlpatterns = [
    path('', views.Profile.as_view()),
    path('update/', views.updateUser),
    path('check-login/', views.chech_login),
    path('get-all/', views.getAllUser)
]
