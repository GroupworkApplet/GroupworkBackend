from rest_framework import serializers
from user.serializers import UserSerializer
from django.contrib.auth.models import User
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'created_time', 'is_read']
