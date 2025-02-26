from django.urls import path
from .views import chatbot_view,chatbot

urlpatterns = [
    path('', chatbot, name='chatbot'),
    path('chatbot/', chatbot_view, name='chatbot_api'),
]
