from django.urls import path
from . import views
urlpatterns = [
    path('', views.ViewPost.as_view()),
    path('comment/', views.Comment.as_view()),
    path('comment/reply/', views.Reply.as_view()),
    path('detail/', views.getDetail),
]
