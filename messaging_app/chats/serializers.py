"""A module for serializing my models."""
from rest_framework import serializers
from .models import User, Conversation, Message

class SerializeUser(serializers.ModelSerializer):
    phone_number_present = serializers.SerializerMethodField()
    def get_phone_number_present(self, obj):
        if obj.phone_number is not None:
            return True
    
    def validate_first_name(self, value):
        if ';' in value:
            raise serializers.ValidationError('name contains ; which makes it vulnerable to injection')
    
    def validate_last_name(self, value):
        if ';' in value:
            raise serializers.ValidationError('name contains ; which makes it vulnerable to injection')
    class Meta:
        model = User
        fields = '__all__'

class SerializeMessage(serializers.ModelSerializer):
    sender_id = serializers.CharField(source='sender_id.user_id', read_only=True)
    conversation_id = serializers.integerField(source='conversation_id.conversation_id')
    class Meta:
        model = Message
        fields = '__all__'

class SerializeConversation(serializers.ModelSerializer):
    messages = SerializeMessage(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = '__all__'
