from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'created_time', 'is_read']

    def create(self, validated_data):
        notification = Notification.objects.create(
            title=validated_data['title'],
            message=validated_data['message']
        )
        return notification
