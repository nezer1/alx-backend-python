from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser, models.Model):
    user_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class Conversation(models.Model):
    conversation_id = models.BigAutoField(primary_key=True)
    participants = models.ManyToManyField(User)
    start_time = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    message_id = models.BigAutoField(primary_key=True)
    conversation_id = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, models.on_delete=CASCADE)
    recipient = models.ForeignKey(User, models.on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True)
    message_body = models.TextField()
