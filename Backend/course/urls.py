from django.urls import path
from . import views

urlpatterns = [
    path('', views.ViewCourse.as_view())
]
