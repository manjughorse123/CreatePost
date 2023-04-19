from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('posts/',PostListCreateAPIView.as_view()),
    path('posts/<int:pk>/',PostListCreateUpdateAPIView.as_view()),
   
]