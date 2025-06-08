from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import SerializeConversation, SerializeMessage

# Create your views here.
class MessageViews(viewsets.ModelViewSet):
    Queryset = Message.objects.all()
    serializer_class = SerializeMessage

class ConversationViews(viewsets.ModelViewSet):
    Queryset = Conversation.objects.all()
    serializer_class = SerializeConversation(messages)
